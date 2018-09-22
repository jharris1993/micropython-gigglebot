# _SYSRANGE_START                              = const(b'\x00')

# _SYSTEM_THRESH_HIGH                          = const(b'\x0C')
# _SYSTEM_THRESH_LOW                           = const(b'\x0E')

# _SYSTEM_SEQUENCE_CONFIG                      = const(b'\x01')
# _SYSTEM_RANGE_CONFIG                         = const(b'\x09')
# _SYSTEM_INTERMEASUREMENT_PERIOD              = const(b'\x04')

# _SYSTEM_INTERRUPT_CONFIG_GPIO                = const(b'\x0A')

# _GPIO_HV_MUX_ACTIVE_HIGH                     = const(b'\x84')

# _SYSTEM_INTERRUPT_CLEAR                      = const(b'\x0B')

# _RESULT_INTERRUPT_STATUS                     = const(b'\x13')
# _RESULT_RANGE_STATUS                         = const(b'\x14')

# _RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN       = const(b'\xBC')
# _RESULT_CORE_RANGING_TOTAL_EVENTS_RTN        = const(b'\xC0')
# _RESULT_CORE_AMBIENT_WINDOW_EVENTS_REF       = const(b'\xD0')
# _RESULT_CORE_RANGING_TOTAL_EVENTS_REF        = const(b'\xD4')
# _RESULT_PEAK_SIGNAL_RATE_REF                 = const(b'\xB6')

# _ALGO_PART_TO_PART_RANGE_OFFSET_MM           = const(b'\x28')

# _I2C_SLAVE_DEVICE_ADDRESS                    = const(b'\x8A')

# _MSRC_CONFIG_CONTROL                         = const(b'\x60')

# _PRE_RANGE_CONFIG_MIN_SNR                    = const(b'\x27')
# _PRE_RANGE_CONFIG_VALID_PHASE_LOW            = const(b'\x56')
# _PRE_RANGE_CONFIG_VALID_PHASE_HIGH           = const(b'\x57')
# _PRE_RANGE_MIN_COUNT_RATE_RTN_LIMIT          = const(b'\x64')

# _FINAL_RANGE_CONFIG_MIN_SNR                  = const(b'\x67')
# _FINAL_RANGE_CONFIG_VALID_PHASE_LOW          = const(b'\x47')
# _FINAL_RANGE_CONFIG_VALID_PHASE_HIGH         = const(b'\x48')
# _FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT = const(b'\x44')

# _PRE_RANGE_CONFIG_SIGMA_THRESH_HI            = const(b'\x61')
# _PRE_RANGE_CONFIG_SIGMA_THRESH_LO            = const(b'\x62')

# _PRE_RANGE_CONFIG_VCSEL_PERIOD               = const(b'\x50')
# _PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI          = const(b'\x51')
# _PRE_RANGE_CONFIG_TIMEOUT_MACROP_LO          = const(b'\x52')

# _SYSTEM_HISTOGRAM_BIN                        = const(b'\x81')
# _HISTOGRAM_CONFIG_INITIAL_PHASE_SELECT       = const(b'\x33')
# _HISTOGRAM_CONFIG_READOUT_CTRL               = const(b'\x55')

# _FINAL_RANGE_CONFIG_VCSEL_PERIOD             = const(b'\x70')
# _FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI        = const(b'\x71')
# _FINAL_RANGE_CONFIG_TIMEOUT_MACROP_LO        = const(b'\x72')
# _CROSSTALK_COMPENSATION_PEAK_RATE_MCPS       = const(b'\x20')

# _MSRC_CONFIG_TIMEOUT_MACROP                  = const(b'\x46')

# _SOFT_RESET_GO2_SOFT_RESET_N                 = const(b'\xBF')
# _IDENTIFICATION_MODEL_ID                     = const(b'\xC0')
# _IDENTIFICATION_REVISION_ID                  = const(b'\xC2')

# _OSC_CALIBRATE_VAL                           = const(b'\xF8')

# _GLOBAL_CONFIG_VCSEL_WIDTH                   = const(b'\x32')
# _GLOBAL_CONFIG_SPAD_ENABLES_REF_0            = const(b'\xB0')
# _GLOBAL_CONFIG_SPAD_ENABLES_REF_1            = const(b'\xB1')
# _GLOBAL_CONFIG_SPAD_ENABLES_REF_2            = const(b'\xB2')
# _GLOBAL_CONFIG_SPAD_ENABLES_REF_3            = const(b'\xB3')
# _GLOBAL_CONFIG_SPAD_ENABLES_REF_4            = const(b'\xB4')
# _GLOBAL_CONFIG_SPAD_ENABLES_REF_5            = const(b'\xB5')

# _GLOBAL_CONFIG_REF_EN_START_SELECT           = const(b'\xB6')
# _DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD         = const(b'\x4E')
# _DYNAMIC_SPAD_REF_EN_START_OFFSET            = const(b'\x4F')
# _POWER_MANAGEMENT_GO1_POWER_FORCE            = const(b'\x80')

# _VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV           = const(b'\x89')

# _ALGO_PHASECAL_LIM                           = const(b'\x30')
# _ALGO_PHASECAL_CONFIG_TIMEOUT                = const(b'\x30')

import microbit
import ustruct
from utime import sleep_ms, ticks_ms
from micropython import const

write = microbit.i2c.write
read = microbit.i2c.read

# import struct
# from time import time, sleep
# from periphery import I2C

# ustruct = struct

# def sleep_ms(ms):
#     sleep(ms / 1000.0)

# def ticks_ms():
#     return int(time() // 1000)

# i2c = I2C('/dev/i2c-1')

# def read(addr, no_bytes):
#     read_bytes = [255] * no_bytes
#     msg = [I2C.Message(read_bytes, read = True)]
#     i2c.transfer(addr, msg)
#     data = msg[0].data

#     return bytes(data)

# def write(addr, data):
#     data = list(struct.unpack('B' * (len(data.hex()) // 2), data))
#     msg = [I2C.Message(data)]
#     i2c.transfer(addr, msg)

_DEFAULT_ADDRESS                             = 0x29
__VL53L0X_VCSEL_PERIOD_RANGE_PRE             = 0
__VL53L0X_VCSEL_PERIOD_RANGE_FINAL           = 1

class VL53L0X():

    io_timeout = 0
    did_timeout = False
    addr = _DEFAULT_ADDRESS

    def __init__(self, address = 0x29, timeout = 500):   
        try:
            write(self.addr, b'\xbf' + b'\x00')
            sleep_ms(2)
        except OSError:
            pass

        write(self.addr, b'\xbf' + b'\x00')
        sleep_ms(5)

        write(self.addr, b'\xbf' + b'\x01')
        sleep_ms(5)

        self.__set_address(address)
        
        write(self.addr, b'\x89')
        write(self.addr, b'\x89' + ustruct.pack('B', (read(self.addr, 1)[0] | 0x01)))

        # "Set I2C standard mode"
        write(self.addr, b'\x88\x00')

        write(self.addr, b'\x80\x01')
        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x00\x00')

        write(self.addr, b'\x91')
        self.stop_variable = read(self.addr, 1)

        write(self.addr, b'\x00\x01')
        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x80\x00')

        # disable SIGNAL_RATE_MSRC (bit 1) and SIGNAL_RATE_PRE_RANGE (bit 4) limit checks
        write(self.addr, b'\x60')
        write(self.addr, b'\x60' + ustruct.pack('B', (read(self.addr, 1)[0] | 0x12)))

        # set final range signal rate limit to 0.25 MCPS (million counts per second)
        self.__set_signal_rate_limit(0.25)

        write(self.addr, b'\x01' + b'\xff')

        spad_count, spad_type_is_aperture, success = self.__get_spad_info()
        if not success:
            self.__set_timeout(timeout)     # set the timeout
            return

        # The SPAD map (RefGoodSpadMap) is read by VL53L0X_get_info_from_device() in
        # the API, but the same data seems to be more easily readable from
        # __VL53L0Xb'\xb0' through _6, so read it from there
        write(self.addr, b'\xb0')
        ref_spad_map = bytearray(read(self.addr, 6))

        # -- VL53L0X_set_reference_spads() begin (assume NVM values are valid)

        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x4f' + b'\x00')
        write(self.addr, b'\x4e' + b'\x2c')
        write(self.addr, b'\xff\x00')
        write(self.addr, b'\xb6' + b'\xb4')

        if spad_type_is_aperture:
            first_spad_to_enable = 12 # 12 is the first aperture spad
        else:
            first_spad_to_enable = 0

        spads_enabled = 0

        i = bytearray(b'\x00')
        while i[0] < 48:
            if i[0] < first_spad_to_enable or spads_enabled == spad_count:
                # This bit is lower than the first one that should be enabled, or
                # (reference_spad_count) bits have already been enabled, so zero this bit
                ref_spad_map[int(i[0] / 8)] &= ~(1 << (i[0] % 8))
            elif (ref_spad_map[int(i[0] / 8)] >> (i[0] % 8)) & 0x1:
                spads_enabled += 1
            i[0] += 1

        write(self.addr, b'\xb0' + ref_spad_map)

        # -- VL53L0X_set_reference_spads() end

        # -- VL53L0X_load_tuning_settings() begin
        # DefaultTuningSettings from vl53l0x_tuning.h

        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x00\x00')

        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x09\x00')
        write(self.addr, b'\x10\x00')
        write(self.addr, b'\x11\x00')

        write(self.addr, b'\x24\x01')
        write(self.addr, b'\x25\xff')
        write(self.addr, b'\x75\x00')

        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x4e\x2c')
        write(self.addr, b'\x48\x00')
        write(self.addr, b'\x30\x20')

        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x30\x09')
        write(self.addr, b'\x54\x00')
        write(self.addr, b'\x31\x04')
        write(self.addr, b'\x32\x03')
        write(self.addr, b'\x40\x83')
        write(self.addr, b'\x46\x25')
        write(self.addr, b'\x60\x00')
        write(self.addr, b'\x27\x00')
        write(self.addr, b'\x50\x06')
        write(self.addr, b'\x51\x00')
        write(self.addr, b'\x52\x96')
        write(self.addr, b'\x56\x08')
        write(self.addr, b'\x57\x30')
        write(self.addr, b'\x61\x00')
        write(self.addr, b'\x62\x00')
        write(self.addr, b'\x64\x00')
        write(self.addr, b'\x65\x00')
        write(self.addr, b'\x66\xa0')

        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x22\x32')
        write(self.addr, b'\x47\x14')
        write(self.addr, b'\x49\xff')
        write(self.addr, b'\x4a\x00')

        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x7a\x0a')
        write(self.addr, b'\x7b\x00')
        write(self.addr, b'\x78\x21')

        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x23\x34')
        write(self.addr, b'\x42\x00')
        write(self.addr, b'\x44\xff')
        write(self.addr, b'\x45\x26')
        write(self.addr, b'\x46\x05')
        write(self.addr, b'\x40\x40')
        write(self.addr, b'\x0e\x06')
        write(self.addr, b'\x20\x1a')
        write(self.addr, b'\x43\x40')

        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x34\x03')
        write(self.addr, b'\x35\x44')

        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x31\x04')
        write(self.addr, b'\x4b\x09')
        write(self.addr, b'\x4c\x05')
        write(self.addr, b'\x4d\x04')

        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x44\x00')
        write(self.addr, b'\x45\x20')
        write(self.addr, b'\x47\x08')
        write(self.addr, b'\x48\x28')
        write(self.addr, b'\x67\x00')
        write(self.addr, b'\x70\x04')
        write(self.addr, b'\x71\x01')
        write(self.addr, b'\x72\xfe')
        write(self.addr, b'\x76\x00')
        write(self.addr, b'\x77\x00')

        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x0d\x01')

        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x80\x01')
        write(self.addr, b'\x01\xf8')

        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x8e\x01')
        write(self.addr, b'\x00\x01')
        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x80\x00')

        # -- VL53L0X_load_tuning_settings() end

        # "Set interrupt config to new sample ready"
        # -- VL53L0X_SetGpioConfig() begin

        write(self.addr, b'\x0a' + b'\x04')
        write(self.addr, b'\x84')
        write(self.addr, b'\x84' + ustruct.pack('B', read(self.addr, 1)[0] & ~0x10))
        write(self.addr, b'\x0b' + b'\x01')

        # -- VL53L0X_SetGpioConfig() end
        self.measurement_timing_budget_us = self.__get_measurement_timing_budget()

        # "Disable MSRC and TCC by default"
        # MSRC = Minimum Signal Rate Check
        # TCC = Target CentreCheck
        # -- VL53L0X_SetSequenceStepEnable() begin

        write(self.addr, b'\x01' + b'\xe8')

        # -- VL53L0X_SetSequenceStepEnable() end

        # "Recalculate timing budget"
        self.__set_measurement_timing_budget(self.measurement_timing_budget_us)

        # VL53L0X_StaticInit() end

        # VL53L0X_PerformRefCalibration() begin (VL53L0X_perform_ref_calibration())

        # -- VL53L0X_perform_vhv_calibration() begin

        write(self.addr, b'\x01' + b'\x01')
        if not self.__perform_single_ref_calibration(0x40):
            self.__set_timeout(timeout)     # set the timeout
            return

        # -- VL53L0X_perform_vhv_calibration() end

        # -- VL53L0X_perform_phase_calibration() begin

        write(self.addr, b'\x01' + b'\x02')
        if not self.__perform_single_ref_calibration(0x00):
            self.__set_timeout(timeout)     # set the timeout
            return

        # -- VL53L0X_perform_phase_calibration() end

        # "restore the previous Sequence Config"
        write(self.addr, b'\x01' + b'\xe8')

        self.__set_timeout(timeout)     # set the timeout

    def __set_address(self, address):
        address &= 0x7f
        try:
            write(self.addr, b'\x8a' + ustruct.pack('B', address))
            self.addr = address
        except IOError:
            write(address, b'\x8a' + ustruct.pack('B', address))
            self.addr = address

    def __set_signal_rate_limit(self, limit_Mcps):
        if (limit_Mcps < 0 or limit_Mcps > 511.99):
            return False
        limit_Mcps = int(limit_Mcps * (1 << 7))

        # Q9.7 fixed point format (9 integer bits, 7 fractional bits)
        write(self.addr, b'\x44' + ustruct.pack('BB', limit_Mcps >> 8 & 0xff, limit_Mcps & 0xff))
        return True

    def __get_spad_info(self):
        write(self.addr, b'\x80\x01')
        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x00\x00')

        write(self.addr, b'\xff\x06')
        write(self.addr, b'\x83')
        write(self.addr, b'\x83' + ustruct.pack('B', read(self.addr, 1)[0] | 0x04))
        write(self.addr, b'\xff\x07')
        write(self.addr, b'\x81\x01')

        write(self.addr, b'\x80\x01')

        write(self.addr, b'\x94\x6b')
        write(self.addr, b'\x83\x00')

        self.__start_timeout()
        write(self.addr, b'\x83')
        while(read(self.addr, 1) == b'\x00'):
            if(self.__check_timeout_expired()):
                return 0, 0, False
            else:
                write(self.addr, b'\x83')

        write(self.addr, b'\x83\x01')
        write(self.addr, b'\x92')
        tmp = read(self.addr, 1)[0]

        count = tmp & 0x7f
        type_is_aperture = (tmp >> 7) & 0x01

        write(self.addr, b'\x81\x00')
        write(self.addr, b'\xff\x06')
        write(self.addr, b'\x83')
        write(self.addr, b'\x83' + ustruct.pack('B', read(self.addr, 1)[0] & ~0x04))
        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x00\x01')

        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x80\x00')

        return count, type_is_aperture, True

    def __check_timeout_expired(self):
        if(self.io_timeout > 0 and (ticks_ms() - self.timeout_start) > self.io_timeout):
            return True
        return False

    def __start_timeout(self):
        self.timeout_start = ticks_ms()

    def __get_measurement_timing_budget(self):
        StartOverhead      = 1910 # note that this is different than the value in set_
        EndOverhead        = 960
        MsrcOverhead       = 660
        TccOverhead        = 590
        DssOverhead        = 690
        PreRangeOverhead   = 660
        FinalRangeOverhead = 550

        # "Start and end overhead times always present"
        budget_us = StartOverhead + EndOverhead

        enables = self.__get_sequence_step_enables()
        timeouts = self.__get_sequence_step_timeouts(enables["pre_range"])

        if (enables["tcc"]):
            budget_us += (timeouts["msrc_dss_tcc_us"] + TccOverhead)

        if (enables["dss"]):
            budget_us += 2 * (timeouts["msrc_dss_tcc_us"] + DssOverhead)
        elif (enables["msrc"]):
            budget_us += (timeouts["msrc_dss_tcc_us"] + MsrcOverhead)

        if (enables["pre_range"]):
            budget_us += (timeouts["pre_range_us"] + PreRangeOverhead)

        if (enables["final_range"]):
            budget_us += (timeouts["final_range_us"] + FinalRangeOverhead)

        self.measurement_timing_budget_us = budget_us # store for internal reuse
        return budget_us

    def __get_sequence_step_enables(self):
        write(self.addr, b'\x01')
        sequence_config = read(self.addr, 1)[0]
        SequenceStepEnables = {"tcc":0, "msrc":0, "dss":0, "pre_range":0, "final_range":0}
        SequenceStepEnables["tcc"]         = (sequence_config >> 4) & 0x1
        SequenceStepEnables["dss"]         = (sequence_config >> 3) & 0x1
        SequenceStepEnables["msrc"]        = (sequence_config >> 2) & 0x1
        SequenceStepEnables["pre_range"]   = (sequence_config >> 6) & 0x1
        SequenceStepEnables["final_range"] = (sequence_config >> 7) & 0x1
        return SequenceStepEnables

    def __get_sequence_step_timeouts(self, pre_range):
        SequenceStepTimeouts = {"pre_range_vcsel_period_pclks":0, "final_range_vcsel_period_pclks":0, "msrc_dss_tcc_mclks":0, "pre_range_mclks":0, "final_range_mclks":0, "msrc_dss_tcc_us":0, "pre_range_us":0, "final_range_us":0}
        SequenceStepTimeouts["pre_range_vcsel_period_pclks"] = self.__get_vcsel_pulse_period(0)

        write(self.addr, b'\x46')
        SequenceStepTimeouts["msrc_dss_tcc_mclks"] = read(self.addr, 1)[0] + 1
        SequenceStepTimeouts["msrc_dss_tcc_us"] = self.__timeout_mclks_to_microseconds(SequenceStepTimeouts["msrc_dss_tcc_mclks"], SequenceStepTimeouts["pre_range_vcsel_period_pclks"])

        write(self.addr, b'\x51')
        SequenceStepTimeouts["pre_range_mclks"] = self.__decode_timeout(ustruct.unpack('>H', read(self.addr, 2))[0])
        SequenceStepTimeouts["pre_range_us"] = self.__timeout_mclks_to_microseconds(SequenceStepTimeouts["pre_range_mclks"], SequenceStepTimeouts["pre_range_vcsel_period_pclks"])

        SequenceStepTimeouts["final_range_vcsel_period_pclks"] = self.__get_vcsel_pulse_period(1)

        write(self.addr, b'\x71')
        SequenceStepTimeouts["final_range_mclks"] = self.__decode_timeout(ustruct.unpack('>H', read(self.addr, 2))[0])

        if (pre_range):
            SequenceStepTimeouts["final_range_mclks"] -= SequenceStepTimeouts["pre_range_mclks"]

        SequenceStepTimeouts["final_range_us"] = self.__timeout_mclks_to_microseconds(SequenceStepTimeouts["final_range_mclks"], SequenceStepTimeouts["final_range_vcsel_period_pclks"])

        return SequenceStepTimeouts

    # Decode VCSEL (vertical cavity surface emitting laser) pulse period in PCLKs
    # from register value
    # based on VL53L0X_decode_vcsel_period()
    def __decode_vcsel_period(self, reg_val):
        return (((reg_val) + 1) << 1)

    # Get the VCSEL pulse period in PCLKs for the given period type.
    # based on VL53L0X_get_vcsel_pulse_period()
    def __get_vcsel_pulse_period(self, type):
        if type == 0:
            write(self.addr, b'\x50')
            return self.__decode_vcsel_period(read(self.addr, 1)[0])
        elif type == 1:
            write(self.addr, b'\x70')
            return self.__decode_vcsel_period(read(self.addr, 1)[0])
        else:
            return 255

    # Convert sequence step timeout from MCLKs to microseconds with given VCSEL period in PCLKs
    # based on VL53L0X_calc_timeout_us()
    def __timeout_mclks_to_microseconds(self, timeout_period_mclks, vcsel_period_pclks):
        macro_period_ns = self.__calc_macro_period(vcsel_period_pclks)
        return ((timeout_period_mclks * macro_period_ns) + (macro_period_ns / 2)) / 1000

    # Calculate macro period in *nanoseconds* from VCSEL period in PCLKs
    # based on VL53L0X_calc_macro_period_ps()
    # PLL_period_ps = 1655; macro_period_vclks = 2304
    def __calc_macro_period(self, vcsel_period_pclks):
        return (((2304 * vcsel_period_pclks * 1655) + 500) / 1000)

    # Decode sequence step timeout in MCLKs from register value
    # based on VL53L0X_decode_timeout()
    # Note: the original function returned a uint32_t, but the return value is
    #always stored in a uint16_t.
    def __decode_timeout(self, reg_val):
        # format: "(LSByte * 2^MSByte) + 1"
        return ((reg_val & 0x00FF) << ((reg_val & 0xFF00) >> 8)) + 1;

    # Set the measurement timing budget in microseconds, which is the time allowed
    # for one measurement the ST API and this library take care of splitting the
    # timing budget among the sub-steps in the ranging sequence. A longer timing
    # budget allows for more accurate measurements. Increasing the budget by a
    # factor of N decreases the range measurement standard deviation by a factor of
    # sqrt(N). Defaults to about 33 milliseconds the minimum is 20 ms.
    # based on VL53L0X_set_measurement_timing_budget_micro_seconds()
    def __set_measurement_timing_budget(self, budget_us):
        StartOverhead      = 1320 # note that this is different than the value in get_
        EndOverhead        = 960
        MsrcOverhead       = 660
        TccOverhead        = 590
        DssOverhead        = 690
        PreRangeOverhead   = 660
        FinalRangeOverhead = 550

        MinTimingBudget = 20000

        if budget_us < MinTimingBudget:
            return False

        used_budget_us = StartOverhead + EndOverhead

        enables = self.__get_sequence_step_enables()
        timeouts = self.__get_sequence_step_timeouts(enables["pre_range"])

        if enables["tcc"]:
            used_budget_us += (timeouts["msrc_dss_tcc_us"] + TccOverhead)

        if enables["dss"]:
            used_budget_us += 2 * (timeouts["msrc_dss_tcc_us"] + DssOverhead)
        elif enables["msrc"]:
            used_budget_us += (timeouts["msrc_dss_tcc_us"] + MsrcOverhead)

        if enables["pre_range"]:
            used_budget_us += (timeouts["pre_range_us"] + PreRangeOverhead)

        if enables["final_range"]:
            used_budget_us += FinalRangeOverhead

            # "Note that the final range timeout is determined by the timing
            # budget and the sum of all other timeouts within the sequence.
            # If there is no room for the final range timeout, then an error
            # will be set. Otherwise the remaining time will be applied to
            # the final range."

            if used_budget_us > budget_us:
                # "Requested timeout too big."
                return False

            final_range_timeout_us = budget_us - used_budget_us

            # set_sequence_step_timeout() begin
            # (SequenceStepId == VL53L0X_SEQUENCESTEP_FINAL_RANGE)

            # "For the final range timeout, the pre-range timeout
            #  must be added. To do this both final and pre-range
            #  timeouts must be expressed in macro periods MClks
            #  because they have different vcsel periods."

            final_range_timeout_mclks = self.__timeout_microseconds_to_mclks(final_range_timeout_us, timeouts["final_range_vcsel_period_pclks"])

            if enables["pre_range"]:
                final_range_timeout_mclks += timeouts["pre_range_mclks"]

            encoded_timeout = self.__encode_timeout(final_range_timeout_mclks)
            write(self.addr, b'\x71' + ustruct.pack('BB', encoded_timeout >> 8 & 0xff, encoded_timeout & 0xff))

            # set_sequence_step_timeout() end
            self.measurement_timing_budget_us = budget_us # store for internal reuse
        return True

    # Encode sequence step timeout register value from timeout in MCLKs
    # based on VL53L0X_encode_timeout()
    # Note: the original function took a uint16_t, but the argument passed to it
    # is always a uint16_t.
    def __encode_timeout(self, timeout_mclks):
        # format: "(LSByte * 2^MSByte) + 1"

        ls_byte = 0
        ms_byte = 0

        if timeout_mclks > 0:
            ls_byte = timeout_mclks - 1

            while ((int(ls_byte) & 0xFFFFFF00) > 0):
                ls_byte /= 2 # >>=
                ms_byte += 1

            return ((ms_byte << 8) | (int(ls_byte) & 0xFF))
        else:
            return 0 

    # Convert sequence step timeout from microseconds to MCLKs with given VCSEL period in PCLKs
    # based on VL53L0X_calc_timeout_mclks()
    def __timeout_microseconds_to_mclks(self, timeout_period_us, vcsel_period_pclks):
        macro_period_ns = self.__calc_macro_period(vcsel_period_pclks)
        return (((timeout_period_us * 1000) + (macro_period_ns / 2)) / macro_period_ns)


    # based on VL53L0X_perform_single_ref_calibration()
    def __perform_single_ref_calibration(self, vhv_init_byte):
        write(self.addr, b'\x00' + ustruct.pack('B', 0x01 | vhv_init_byte)) # VL53L0X_REG_SYSRANGE_MODE_START_STOP

        self.__start_timeout()
        write(self.addr, b'\x13')
        while (read(self.addr, 1)[0] & 0x07) == 0:
            if self.__check_timeout_expired():
                return False
            else:
                write(self.addr, b'\x13')

        write(self.addr, b'\x0b' + b'\x01')
        write(self.addr, b'\x00' + b'\x00')

        return True

    def __set_timeout(self, timeout):
        self.io_timeout = timeout

    # Start continuous ranging measurements. If period_ms (optional) is 0 or not
    # given, continuous back-to-back mode is used (the sensor takes measurements as 
    # often as possible) otherwise, continuous timed mode is used, with the given
    # inter-measurement period in milliseconds determining how often the sensor
    # takes a measurement.
    # based on VL53L0X_StartMeasurement()
    def start_continuous(self, period_ms = 0):
        write(self.addr, b'\x80\x01')
        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x00\x00')
        write(self.addr, b'\x91' + self.stop_variable)
        write(self.addr, b'\x00\x01')
        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x80\x00')

        if period_ms != 0:
            # continuous timed mode

            # VL53L0X_SetInterMeasurementPeriodMilliSeconds() begin
            write(self.addr, b'\xf8')
            osc_calibrate_val = ustruct.unpack('>H', read(self.addr, 2))[0]

            if osc_calibrate_val != 0:
                period_ms *= osc_calibrate_val

            write(self.addr, b'\x04' + ustruct.pack('>I', period_ms))

            # VL53L0X_SetInterMeasurementPeriodMilliSeconds() end

            write(self.addr, b'\x00' + b'\x04') # VL53L0X_REG_SYSRANGE_MODE_TIMED
        else:
            # continuous back-to-back mode
            write(self.addr, b'\x00' + b'\x02') # VL53L0X_REG_SYSRANGE_MODE_BACKTOBACK
    
    # Returns a range reading in millimeters when continuous mode is active
    # (read_range_single_millimeters() also calls this function after starting a
    # single-shot range measurement)
    def read_range_continuous_millimeters(self):
        self.__start_timeout()
        write(self.addr, b'\x13')
        while ((read(self.addr, 1)[0] & 0x07) == 0):
            if self.__check_timeout_expired():
                self.did_timeout = True
                raise OSError("read_range_continuous_millimeters timeout")
            else:
                write(self.addr, b'\x13')

        # assumptions: Linearity Corrective Gain is 1000 (default)
        # fractional ranging is not enabled
        write(self.addr,  ustruct.pack('B', b'\x14'[0] + 10))
        range = ustruct.unpack('>H', read(self.addr, 2))

        write(self.addr, b'\x0b' + b'\x01')

        return range

    def read_range_single_millimeters(self):
        write(self.addr, b'\x80\x01')
        write(self.addr, b'\xff\x01')
        write(self.addr, b'\x00\x00')
        write(self.addr, b'\x91' + self.stop_variable)
        write(self.addr, b'\x00\x01')
        write(self.addr, b'\xff\x00')
        write(self.addr, b'\x80\x00')

        write(self.addr, b'\x00' + b'\x01')

        # "Wait until start bit has been cleared"
        self.__start_timeout()
        write(self.addr, b'\x00')
        while (read(self.addr, 1)[0] & 0x01):
            if self.__check_timeout_expired():
                self.did_timeout = True
                raise OSError("read_range_single_millimeters timeout")
            else:
                write(self.addr, b'\x00')
        return self.read_range_continuous_millimeters()

    def timeout_occurred(self):
        tmp = self.did_timeout
        self.did_timeout = False
        return tmp

    # Set the VCSEL (vertical cavity surface emitting laser) pulse period for the
    # given period type (pre-range or final range) to the given value in PCLKs.
    # Longer periods seem to increase the potential range of the sensor.
    # Valid values are (even numbers only):
    #  pre:  12 to 18 (initialized default: 14)
    #  final: 8 to 14 (initialized default: 10)
    # based on VL53L0X_setVcselPulsePeriod()
    def __set_vcsel_pulse_period(self, type, period_pclks):
        vcsel_period_reg = self.__encode_vcsel_period(period_pclks)

        enables = self.__get_sequence_step_enables()
        timeouts = self.__get_sequence_step_timeouts(enables["pre_range"])

        # "Apply specific settings for the requested clock period"
        # "Re-calculate and apply timeouts, in macro periods"

        # "When the VCSEL period for the pre or final range is changed,
        # the corresponding timeout must be read from the device using
        # the current VCSEL period, then the new VCSEL period can be
        # applied. The timeout then must be written back to the device
        # using the new VCSEL period.
        #
        # For the MSRC timeout, the same applies - this timeout being
        # dependant on the pre-range vcsel period."

        if type == 0:
            # "Set phase check limits"
            if period_pclks == 12:
                write(self.addr, b'\x57' + b'\x18')
            elif period_pclks == 14:
                write(self.addr, b'\x57' + b'\x30')
            elif period_pclks == 16:
                write(self.addr, b'\x57' + b'\x40')
            elif period_pclks == 18:
                write(self.addr, b'\x57' + b'\x50')
            else:
                return False

            write(self.addr, b'\x56' + b'\x08')

            # apply new VCSEL period
            write(self.addr, b'\x50' + ustruct.pack('B', vcsel_period_reg))

            # update timeouts

            # set_sequence_step_timeout() begin
            # (SequenceStepId == VL53L0X_SEQUENCESTEP_PRE_RANGE)

            new_pre_range_timeout_mclks = self.__timeout_microseconds_to_mclks(timeouts["pre_range_us"], period_pclks)

            encoded_timeout = self.__encode_timeout(new_pre_range_timeout_mclks)
            write(self.addr, b'\x51' + ustruct.pack('BB', encoded_timeout >> 8 & 0xff, encoded_timeout & 0xff))

            # set_sequence_step_timeout() end

            # set_sequence_step_timeout() begin
            # (SequenceStepId == VL53L0X_SEQUENCESTEP_MSRC)

            new_msrc_timeout_mclks = self.__timeout_microseconds_to_mclks(timeouts["msrc_dss_tcc_us"], period_pclks)

            if new_msrc_timeout_mclks > 256:
                write(self.addr, b'\x46' + b'\xff')
            else:
                write(self.addr, b'\x46' + ustruct.pack('B', new_msrc_timeout_mclks - 1))

            # set_sequence_step_timeout() end
        elif type == 1:
            if period_pclks == 8:
                write(self.addr, b'\x48' + b'\x10')
                write(self.addr, b'\x47' + b'\x08')
                write(self.addr, b'\x32' + b'\x02')
                write(self.addr, b'\x30' + b'\x0c')
                write(self.addr, b'\xff\x01')
                write(self.addr, b'\x30' + b'\x30')
                write(self.addr, b'\xff\x00')
            elif period_pclks == 10:
                write(self.addr, b'\x48' + b'\x28')
                write(self.addr, b'\x47' + b'\x08')
                write(self.addr, b'\x32' + b'\x03')
                write(self.addr, b'\x30' + b'\x09')
                write(self.addr, b'\xff\x01')
                write(self.addr, b'\x30' + b'\x20')
                write(self.addr, b'\xff\x00')
            elif period_pclks == 12:
                write(self.addr, b'\x48' + b'\x38')
                write(self.addr, b'\x47' + b'\x08')
                write(self.addr, b'\x32' + b'\x03')
                write(self.addr, b'\x30' + b'\x08')
                write(self.addr, b'\xff\x01')
                write(self.addr, b'\x30' + b'\x20')
                write(self.addr, b'\xff\x00')
            elif period_pclks == 14:
                write(self.addr, b'\x48' + b'\x48')
                write(self.addr, b'\x47' + b'\x08')
                write(self.addr, b'\x32' + b'\x03')
                write(self.addr, b'\x30' + b'\x07')
                write(self.addr, b'\xff\x01')
                write(self.addr, b'\x30' + b'\x20')
                write(self.addr, b'\xff\x00')
            else:
                # invalid period
                return False

            # apply new VCSEL period
            write(self.addr, b'\x70' + ustruct.pack('B', vcsel_period_reg))

            # update timeouts

            # set_sequence_step_timeout() begin
            # (SequenceStepId == VL53L0X_SEQUENCESTEP_FINAL_RANGE)

            # "For the final range timeout, the pre-range timeout
            #  must be added. To do this both final and pre-range
            #  timeouts must be expressed in macro periods MClks
            #  because they have different vcsel periods."

            new_final_range_timeout_mclks = self.__timeout_microseconds_to_mclks(timeouts["final_range_us"], period_pclks)

            if enables["pre_range"]:
                new_final_range_timeout_mclks += timeouts["pre_range_mclks"]

            encoded_timeout = self.__encode_timeout(new_final_range_timeout_mclks)
            write(self.addr, b'\x71' + ustruct.pack('BB', encoded_timeout >> 8 & 0xff, encoded_timeout & 0xff))

            # set_sequence_step_timeout end
        else:
            # invalid type
            return False

        # "Finally, the timing budget must be re-applied"

        self.__set_measurement_timing_budget(measurement_timing_budget_us)

        # "Perform the phase calibration. This is needed after changing on vcsel period."
        write(self.addr, b'\x01')
        sequence_config = read(self.addr, 1)
        write(self.addr, b'\x01' + b'\x02')
        self.__perform_single_ref_calibration(0x0)
        write(self.addr, b'\x01' + sequence_config)

        return True

    # Encode VCSEL pulse period register value from period in PCLKs
    # based on VL53L0X_encode_vcsel_period()
    def __encode_vcsel_period(self, period_pclks):
        return((period_pclks >> 1) - 1)