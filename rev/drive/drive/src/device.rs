use std::io::Read;
use std::io::Write;

pub trait Device {
    fn get_byte(&mut self) -> u8;
    fn send_byte(&mut self, byte: u8);
}

pub struct Reader<'a> {
    pub reader: &'a mut dyn Read,
}

impl Device for Reader<'_> {
    fn get_byte(&mut self) -> u8 {
        self.reader
            .bytes()
            .next()
            .and_then(|result| result.ok())
            .map(|byte| byte as u8)
            .unwrap()
    }

    fn send_byte(&mut self, _byte: u8) {}
}

pub struct Tape {
    pub tape: [u8; 25000],
    pub index: usize,
}

impl Device for Tape {
    fn get_byte(&mut self) -> u8 {
        if self.index == 0 {
            self.index = 25000;
        }
        self.index -= 1;
        self.index %= 25000;
        self.tape[self.index]
    }

    fn send_byte(&mut self, byte: u8) {
        self.tape[self.index] = byte;
        self.index += 1;
        self.index %= 25000;
    }
}

pub struct Writer<'a> {
    pub writer: &'a mut dyn Write,
}

impl Device for Writer<'_> {
    fn get_byte(&mut self) -> u8 {
        0
    }

    fn send_byte(&mut self, byte: u8) {
        self.writer.write_all(&[byte]).unwrap();
    }
}

pub struct Arithmetic {
    pub buffer: [u8; 3],
    pub index: usize,
}

impl Device for Arithmetic {
    fn get_byte(&mut self) -> u8 {
        match self.buffer[2] {
            0 => self.buffer[0].overflowing_mul(self.buffer[1]).0,
            1 => self.buffer[0].overflowing_add(self.buffer[1]).0,
            2 => self.buffer[0].overflowing_sub(self.buffer[1]).0,
            3 => self.buffer[0] ^ self.buffer[1],
            4 => self.buffer[0].overflowing_div(self.buffer[1]).0,
            5 => self.buffer[0] % self.buffer[1],
            _ => 0,
        }
    }

    fn send_byte(&mut self, byte: u8) {
        self.buffer[self.index] = byte;
        self.index += 1;
        self.index %= 3;
    }
}
