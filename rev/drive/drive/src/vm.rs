use crate::device::Device;

#[repr(C)]
pub struct State<'a> {
    pub ip: usize,
    pub mem: [u8; 4],
    pub program: Vec<u8>,
    pub devices: Vec<Box<dyn Device + 'a>>,
}

impl State<'_> {
    #[inline(never)]
    fn next_byte(&mut self) -> u8 {
        let result = self.program[self.ip];
        self.ip += 1;
        result
    }

    #[inline(never)]
    fn next_word(&mut self) -> u16 {
        let result = (u16::from(self.program[self.ip]) << 8) | u16::from(self.program[self.ip + 1]);
        self.ip += 2;
        result
    }

    #[inline(never)]
    fn next_dword(&mut self) -> u32 {
        let result = (u32::from(self.program[self.ip]) << 24)
            | (u32::from(self.program[self.ip + 1]) << 16)
            | (u32::from(self.program[self.ip + 2]) << 8)
            | (u32::from(self.program[self.ip + 3]));
        self.ip += 4;
        result
    }
}

#[repr(C)]
pub enum Opcode {
    Nop,
    Halt,
    Load,
    r#Send,
    Get,
    Less,
    LessEq,
}

impl From<u8> for Opcode {
    fn from(v: u8) -> Self {
        match v {
            0x00 => Opcode::Nop,
            0x01 => Opcode::Halt,
            0x10 => Opcode::Load,
            0x20 => Opcode::r#Send,
            0x21 => Opcode::Get,
            0x50 => Opcode::Less,
            0x51 => Opcode::LessEq,
            _ => Opcode::Halt,
        }
    }
}

pub fn vm_run(mut state: State) -> i32 {
    loop {
        if state.ip >= state.program.len() {
            return 1;
        }
        match Opcode::from(state.program[state.ip]) {
            Opcode::Nop => {
                state.ip += 1;
            }
            Opcode::Halt => {
                state.ip += 1;
                let ret = state.next_byte();
                return ret as i32;
            }
            Opcode::Load => {
                state.ip += 1;
                let location = state.next_byte() as usize;
                let value = state.next_byte();
                state.mem[location] = value;
            }
            Opcode::r#Send => {
                state.ip += 1;
                let device = state.next_byte() as usize;
                let mem = state.mem[state.next_byte() as usize];
                state.devices[device].send_byte(mem);
            }
            Opcode::Get => {
                state.ip += 1;
                let mem = state.next_byte() as usize;
                let device = state.next_byte() as usize;
                state.mem[mem] = state.devices[device].get_byte();
            }
            Opcode::Less => {
                state.ip += 1;
                let mem1 = state.mem[state.next_byte() as usize];
                let mem2 = state.mem[state.next_byte() as usize];
                let jump = state.next_word() as usize;
                if mem1 < mem2 {
                    state.ip = jump;
                }
            }
            Opcode::LessEq => {
                state.ip += 1;
                let mem1 = state.mem[state.next_byte() as usize];
                let mem2 = state.mem[state.next_byte() as usize];
                let jump = state.next_word() as usize;
                if mem1 <= mem2 {
                    state.ip = jump;
                }
            }
        }
    }
}
