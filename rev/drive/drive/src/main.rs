#![allow(dead_code)]

mod device;
mod vm;

use device::{Arithmetic, Reader, Tape, Writer};
use rand::prelude::random;
use std::fs;
use std::io;
use std::io::Cursor;
use std::io::Read;
use vm::{vm_run, State};

fn main() {
    let program: Vec<u8> = io::stdin()
        .bytes()
        .map(|res| res.unwrap_or_else(|_| std::process::exit(1)))
        .collect();

    for _ in 0..10 {
        let iv: [u8; 4] = random();
        let mut input = Cursor::new(iv);
        let mut output = Cursor::new(vec![0, 0, 0, 0]);

        let state = State {
            ip: 0usize,
            mem: [0; 4],
            program: program.clone(),
            devices: vec![
                Box::new(Reader { reader: &mut input }),
                Box::new(Writer {
                    writer: &mut output,
                }),
                Box::new(Arithmetic {
                    buffer: [0; 3],
                    index: 0usize,
                }),
                Box::new(Tape {
                    tape: [0; 25000],
                    index: 0usize,
                }),
            ],
        };
        vm_run(state);
        let ov: [u8; 4] = output.into_inner().try_into().unwrap();
        if ov != encrypt(iv) {
            std::process::exit(1);
        }
    }
    println!(
        "{}",
        fs::read_to_string("flag.txt").unwrap_or_else(|_| {
            println!("Couldn't open flag file, please contact an admin if on the server.");
            std::process::exit(1)
        })
    );
}

#[inline(never)]
fn encrypt(block: [u8; 4]) -> [u8; 4] {
    let mut block = block;

    #[allow(clippy::clone_on_copy)]
    let mut b = block.clone();

    let (i, _) = block[0].overflowing_add(block[3]);
    b[1] ^= i;
    let (i, _) = block[1].overflowing_add(block[0]);
    b[2] ^= i;
    let (i, _) = block[2].overflowing_add(block[1]);
    b[3] ^= i;
    let (i, _) = block[3].overflowing_add(block[2]);
    b[0] ^= i;

    block = b;

    for _ in 0..block[3] {
        let (mul, _) = block[2].overflowing_mul(block[0]);
        let (sum, _) = mul.overflowing_add(block[1]);
        block[0] = sum % block[3];
    }

    block
}
