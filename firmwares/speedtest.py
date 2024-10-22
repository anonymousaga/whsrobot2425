import os
import utime
from machine import freq
freq(250000000)

start_time = utime.ticks_ms()
for i in range(3,160000):
    e=(i+38472.3523)**(1598.324/i)
end_time = utime.ticks_ms()

elapsed_time = utime.ticks_diff(end_time, start_time)

print("Elapsed time:", elapsed_time, "ms") 

# Pi pico 2, 250 kHz, 250RPI_PICO2-RISCV-20241022-v1.24.0-preview.461.g3f54e5dff.uf2, 8768 ms
# Pi pico 2, 300 kHz, 250RPI_PICO2-RISCV-20241022-v1.24.0-preview.461.g3f54e5dff.uf2, 7306 ms
# Pi pico 2, 250 kHz, RPI_PICO2-20241022-v1.24.0-preview.461.g3f54e5dff.uf2, 1758 ms !!!
# Pi pico 2, 300 kHz, RPI_PICO2-20241022-v1.24.0-preview.461.g3f54e5dff.uf2, 1466 ms !!!
# Pi pico, 250 kHz, 250RPI_PICO2-RISCV-20241022-v1.24.0-preview.461.g3f54e5dff.uf2, 9287 ms

