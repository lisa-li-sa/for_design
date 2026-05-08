/**
 * @file rtl_test_params.c
 * @brief RTL Test Parameter Block for TensorStore ISA-Test Kernel
 *
 * Defines the kernel parameter array placed at 0xA0000100 (DTCM base + 0x100).
 * The C++ simulator (tensorstore_isa_test_rtl_sim_v2) overwrites this region
 * at runtime before triggering CMD FIFO dispatch.
 *
 * Parameter layout (tensorstore_isa_test):
 *   [0] acc_addr         - Input / accumulator base address
 *   [1] broadcast_data   - Scalar for MAX/MIN (IEEE-754 float bits)
 *   [2] max_tdatatype    - dtype encoding for MAX mode (0=INT8 1=INT16 2=INT32 3=FP16 4=FP32)
 *   [3] min_tdatatype    - dtype encoding for MIN mode
 *   [4] tensorstore_mode - Operation mode (0=POP 1=CVT16 2=CVT32 3=MAX 4=MIN)
 *   [5] fraction_bit     - Fraction bits for CVT16/CVT32 conversion
 */

#include <stdint.h>

/* Placed in .ts_params section; linker script maps this to 0xA0000100.
 * Initialised to sensible defaults; the simulator writes real values
 * before launch. */
volatile uint32_t rtl_test_params[6] __attribute__((section(".ts_params"))) = {
    0x00004000,  /* [0] acc_addr        - input accumulator base */
    0,           /* [1] broadcast_data  - 0.0f (no broadcast) */
    4,           /* [2] max_tdatatype   - dtype=FP32(4) */
    4,           /* [3] min_tdatatype   - dtype=FP32(4) */
    0,           /* [4] tensorstore_mode - 0=TS_MODE_POP (pass-through) */
    0,           /* [5] fraction_bit    - 0 (no fractional shift) */
};
