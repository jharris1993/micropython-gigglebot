import microbit
import ustruct
from utime import sleep_ms, 
from micropython import const

_SYSRANGE_START                              = const(b'\x00')

_SYSTEM_THRESH_HIGH                          = const(b'\x0C')
_SYSTEM_THRESH_LOW                           = const(b'\x0E')

_SYSTEM_SEQUENCE_CONFIG                      = const(b'\x01')
_SYSTEM_RANGE_CONFIG                         = const(b'\x09')
_SYSTEM_INTERMEASUREMENT_PERIOD              = const(b'\x04')

_SYSTEM_INTERRUPT_CONFIG_GPIO                = const(b'\x0A')

_GPIO_HV_MUX_ACTIVE_HIGH                     = const(b'\x84')

_SYSTEM_INTERRUPT_CLEAR                      = const(b'\x0B')

_RESULT_INTERRUPT_STATUS                     = const(b'\x13')
_RESULT_RANGE_STATUS                         = const(b'\x14')

_RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN       = const(b'\xBC')
_RESULT_CORE_RANGING_TOTAL_EVENTS_RTN        = const(b'\xC0')
_RESULT_CORE_AMBIENT_WINDOW_EVENTS_REF       = const(b'\xD0')
_RESULT_CORE_RANGING_TOTAL_EVENTS_REF        = const(b'\xD4')
_RESULT_PEAK_SIGNAL_RATE_REF                 = const(b'\xB6')

_ALGO_PART_TO_PART_RANGE_OFFSET_MM           = const(b'\x28')

_I2C_SLAVE_DEVICE_ADDRESS                    = const(b'\x8A')

_MSRC_CONFIG_CONTROL                         = const(b'\x60')

_PRE_RANGE_CONFIG_MIN_SNR                    = const(b'\x27')
_PRE_RANGE_CONFIG_VALID_PHASE_LOW            = const(b'\x56')
_PRE_RANGE_CONFIG_VALID_PHASE_HIGH           = const(b'\x57')
_PRE_RANGE_MIN_COUNT_RATE_RTN_LIMIT          = const(b'\x64')

_FINAL_RANGE_CONFIG_MIN_SNR                  = const(b'\x67')
_FINAL_RANGE_CONFIG_VALID_PHASE_LOW          = const(b'\x47')
_FINAL_RANGE_CONFIG_VALID_PHASE_HIGH         = const(b'\x48')
_FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT = const(b'\x44')

_PRE_RANGE_CONFIG_SIGMA_THRESH_HI            = const(b'\x61')
_PRE_RANGE_CONFIG_SIGMA_THRESH_LO            = const(b'\x62')

_PRE_RANGE_CONFIG_VCSEL_PERIOD               = const(b'\x50')
_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI          = const(b'\x51')
_PRE_RANGE_CONFIG_TIMEOUT_MACROP_LO          = const(b'\x52')

_SYSTEM_HISTOGRAM_BIN                        = const(b'\x81')
_HISTOGRAM_CONFIG_INITIAL_PHASE_SELECT       = const(b'\x33')
_HISTOGRAM_CONFIG_READOUT_CTRL               = const(b'\x55')

_FINAL_RANGE_CONFIG_VCSEL_PERIOD             = const(b'\x70')
_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI        = const(b'\x71')
_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_LO        = const(b'\x72')
_CROSSTALK_COMPENSATION_PEAK_RATE_MCPS       = const(b'\x20')

_MSRC_CONFIG_TIMEOUT_MACROP                  = const(b'\x46')

_SOFT_RESET_GO2_SOFT_RESET_N                 = const(b'\xBF')
_IDENTIFICATION_MODEL_ID                     = const(b'\xC0')
_IDENTIFICATION_REVISION_ID                  = const(b'\xC2')

_OSC_CALIBRATE_VAL                           = const(b'\xF8')

_GLOBAL_CONFIG_VCSEL_WIDTH                   = const(b'\x32')
_GLOBAL_CONFIG_SPAD_ENABLES_REF_0            = const(b'\xB0')
_GLOBAL_CONFIG_SPAD_ENABLES_REF_1            = const(b'\xB1')
_GLOBAL_CONFIG_SPAD_ENABLES_REF_2            = const(b'\xB2')
_GLOBAL_CONFIG_SPAD_ENABLES_REF_3            = const(b'\xB3')
_GLOBAL_CONFIG_SPAD_ENABLES_REF_4            = const(b'\xB4')
_GLOBAL_CONFIG_SPAD_ENABLES_REF_5            = const(b'\xB5')

_GLOBAL_CONFIG_REF_EN_START_SELECT           = const(b'\xB6')
_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD         = const(b'\x4E')
_DYNAMIC_SPAD_REF_EN_START_OFFSET            = const(b'\x4F')
_POWER_MANAGEMENT_GO1_POWER_FORCE            = const(b'\x80')

_VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV           = const(b'\x89')

_ALGO_PHASECAL_LIM                           = const(b'\x30')
_ALGO_PHASECAL_CONFIG_TIMEOUT                = const(b'\x30')
__VL53L0X_VCSEL_PERIOD_RANGE_PRE             = const(0)
__VL53L0X_VCSEL_PERIOD_RANGE_FINAL           = const(1)


_DEFAULT_ADDRESS = const(b'\x29')
_ADDRESS = _DEFAULT_ADDRESS

write = microbit.i2c.write
read = microbit.i2c.read

def VL53L0X_init(address = 0x2A, timeout = 500):

    try:
        write(_ADDRESS, _SOFT_RESET_GO2_SOFT_RESET_N + b'\x00')
        sleep_ms(2)
    except OSError:
        pass

    write(_ADDRESS, _SOFT_RESET_GO2_SOFT_RESET_N + b'\x00')
    sleep_ms(5)

    write(_ADDRESS, _SOFT_RESET_GO2_SOFT_RESET_N + b'\x01')
    sleep_ms(5)


    _VL53L0X_set_address(adress)
    _VL53L0X_init()                   # initialize the sensor
    _VL53L0X_set_timeout(timeout)     # set the timeout

def _VL53L0X_set_address(address):
    address &= 0x7f
    try:
        write(_ADDRESS, _I2C_SLAVE_DEVICE_ADDRESS + ustruct.pack('B', address))
        _ADDRESS = address
    except IOError:
        write(address, _I2C_SLAVE_DEVICE_ADDRESS + ustruct.pack('B', address))
        _ADDRESS = address

def _VL53L0X_init():
    write(_ADDRESS, _VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV)
    write(_ADDRESS, _VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV + ustruct.pack('B', (read(_ADDRESS, 1)[0] | 0x01)))

    # "Set I2C standard mode"
    write(_ADDRESS, b'\x88\x00')

    write(_ADDRESS, b'\x80\x01')
    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x00\x00')
    
    global stop_variable
    write(_ADDRESS, b'\x91')
    stop_variable = read(_ADDRESS, 1)

    write(_ADDRESS, b'\x00\x01')
    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x80\x00')

    # disable SIGNAL_RATE_MSRC (bit 1) and SIGNAL_RATE_PRE_RANGE (bit 4) limit checks
    write(_ADDRESS, _MSRC_CONFIG_CONTROL)
    write(_ADDRESS, _MSRC_CONFIG_CONTROL + ustruct.pack('B', (read(_ADDRESS, 1)[0] | 0x12)))

    # set final range signal rate limit to 0.25 MCPS (million counts per second)
    _VL53L0X_set_signal_rate_limit(0.25)

    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG + b'\xff')

    spad_count, spad_type_is_aperture, success = _VL53L0X_get_spad_info()
    if not success:
        return False

    # The SPAD map (RefGoodSpadMap) is read by VL53L0X_get_info_from_device() in
    # the API, but the same data seems to be more easily readable from
    # __VL53L0X_GLOBAL_CONFIG_SPAD_ENABLES_REF_0 through _6, so read it from there
    write(_ADDRESS, _GLOBAL_CONFIG_SPAD_ENABLES_REF_0)
    ref_spad_map = bytearray(read(_ADDRESS, 6))

    # -- VL53L0X_set_reference_spads() begin (assume NVM values are valid)

    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, _DYNAMIC_SPAD_REF_EN_START_OFFSET + b'\x00')
    write(_ADDRESS, _DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD + b'\x2c')
    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, _GLOBAL_CONFIG_REF_EN_START_SELECT + b'\xb4')

    if spad_type_is_aperture:
        first_spad_to_enable = 12 # 12 is the first aperture spad
    else:
        first_spad_to_enable = 0

    spads_enabled = 0

    i = bytearray(b'\x00')
    while i < 48:
        if i < first_spad_to_enable or spads_enabled == spad_count:
            # This bit is lower than the first one that should be enabled, or
            # (reference_spad_count) bits have already been enabled, so zero this bit
            ref_spad_map[int(i / 8)] &= ~(1 << (i % 8))
        elif (ref_spad_map[int(i / 8)] >> (i % 8)) & 0x1:
            spads_enabled += 1

    write(_ADDRESS, _GLOBAL_CONFIG_SPAD_ENABLES_REF_0 + ref_spad_map)

    # -- VL53L0X_set_reference_spads() end

    # -- VL53L0X_load_tuning_settings() begin
    # DefaultTuningSettings from vl53l0x_tuning.h

    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x00\x00')

    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x09\x00')
    write(_ADDRESS, b'\x10\x00')
    write(_ADDRESS, b'\x11\x00')

    write(_ADDRESS, b'\x24\x01')
    write(_ADDRESS, b'\x25\xff')
    write(_ADDRESS, b'\x75\x00')

    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x4e\x2c')
    write(_ADDRESS, b'\x48\x00')
    write(_ADDRESS, b'\x30\x20')

    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x30\x09')
    write(_ADDRESS, b'\x54\x00')
    write(_ADDRESS, b'\x31\x04')
    write(_ADDRESS, b'\x32\x03')
    write(_ADDRESS, b'\x40\x83')
    write(_ADDRESS, b'\x46\x25')
    write(_ADDRESS, b'\x60\x00')
    write(_ADDRESS, b'\x27\x00')
    write(_ADDRESS, b'\x50\x06')
    write(_ADDRESS, b'\x51\x00')
    write(_ADDRESS, b'\x52\x96')
    write(_ADDRESS, b'\x56\x08')
    write(_ADDRESS, b'\x57\x30')
    write(_ADDRESS, b'\x61\x00')
    write(_ADDRESS, b'\x62\x00')
    write(_ADDRESS, b'\x64\x00')
    write(_ADDRESS, b'\x65\x00')
    write(_ADDRESS, b'\x66\xa0')

    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x22\x32')
    write(_ADDRESS, b'\x47\x14')
    write(_ADDRESS, b'\x49\xff')
    write(_ADDRESS, b'\x4a\x00')

    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x7a\x0a')
    write(_ADDRESS, b'\x7b\x00')
    write(_ADDRESS, b'\x78\x21')

    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x23\x34')
    write(_ADDRESS, b'\x42\x00')
    write(_ADDRESS, b'\x44\xff')
    write(_ADDRESS, b'\x45\x26')
    write(_ADDRESS, b'\x46\x05')
    write(_ADDRESS, b'\x40\x40')
    write(_ADDRESS, b'\x0e\x06')
    write(_ADDRESS, b'\x20\x1a')
    write(_ADDRESS, b'\x43\x40')

    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x34\x03')
    write(_ADDRESS, b'\x35\x44')

    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x31\x04')
    write(_ADDRESS, b'\x4b\x09')
    write(_ADDRESS, b'\x4c\x05')
    write(_ADDRESS, b'\x4d\x04')

    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x44\x00')
    write(_ADDRESS, b'\x45\x20')
    write(_ADDRESS, b'\x47\x08')
    write(_ADDRESS, b'\x48\x28')
    write(_ADDRESS, b'\x67\x00')
    write(_ADDRESS, b'\x70\x04')
    write(_ADDRESS, b'\x71\x01')
    write(_ADDRESS, b'\x72\xfe')
    write(_ADDRESS, b'\x76\x00')
    write(_ADDRESS, b'\x77\x00')

    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x0d\x01')

    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x80\x01')
    write(_ADDRESS, b'\x01\xf8')

    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x8e\x01')
    write(_ADDRESS, b'\x00\x01')
    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x80\x00')

    # -- VL53L0X_load_tuning_settings() end

    # "Set interrupt config to new sample ready"
    # -- VL53L0X_SetGpioConfig() begin

    write(_ADDRESS, _SYSTEM_INTERRUPT_CONFIG_GPIO + b'\x04')
    write(_ADDRESS, _GPIO_HV_MUX_ACTIVE_HIGH)
    write(_ADDRESS, _GPIO_HV_MUX_ACTIVE_HIGH + ustruct.pack('B', read(_ADDRESS, 1)[0] & ~0x10))
    write(_ADDRESS, _SYSTEM_INTERRUPT_CLEAR + b'\x01')

    # -- VL53L0X_SetGpioConfig() end
    global measurement_timing_budget_us
    measurement_timing_budget_us = _VL53L0X_get_measurement_timing_budget()

    # "Disable MSRC and TCC by default"
    # MSRC = Minimum Signal Rate Check
    # TCC = Target CentreCheck
    # -- VL53L0X_SetSequenceStepEnable() begin

    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG + b'\xe8')

    # -- VL53L0X_SetSequenceStepEnable() end

    # "Recalculate timing budget"
    _VL53L0X_set_measurement_timing_budget(measurement_timing_budget_us)

    # VL53L0X_StaticInit() end

    # VL53L0X_PerformRefCalibration() begin (VL53L0X_perform_ref_calibration())

    # -- VL53L0X_perform_vhv_calibration() begin

    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG + b'\x01')
    if not _VL53L0X_perform_single_ref_calibration(0x40):
        return False

    # -- VL53L0X_perform_vhv_calibration() end

    # -- VL53L0X_perform_phase_calibration() begin

    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG + b'\x02')
    if not _VL53L0X_perform_single_ref_calibration(0x00):
        return False

    # -- VL53L0X_perform_phase_calibration() end

    # "restore the previous Sequence Config"
    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG + b'\xe8')

    # VL53L0X_PerformRefCalibration() end

    return True
# Set the return signal rate limit check value in units of MCPS (mega counts
# per second). "This represents the amplitude of the signal reflected from the
# target and detected by the device"; setting this limit presumably determines
# the minimum measurement necessary for the sensor to report a valid reading.
# Setting a lower limit increases the potential range of the sensor but also
# seems to increase the likelihood of getting an inaccurate reading because of
# unwanted reflections from objects other than the intended target.
# Defaults to 0.25 MCPS as initialized by the ST API and this library.
def _VL53L0X_set_signal_rate_limit(limit_Mcps):
    if (limit_Mcps < 0 or limit_Mcps > 511.99):
        return False
    limit_Mcps = int(limit_Mcps * (1 << 7))

    # Q9.7 fixed point format (9 integer bits, 7 fractional bits)
    write(_ADDRESS, _FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT + ustruct.pack('BB', limit_Mcps >> 8 & 0xff, limit_Mcps & 0xff))
    return True

# Get reference SPAD (single photon avalanche diode) count and type
# based on VL53L0X_get_info_from_device(),
# but only gets reference SPAD count and type
def _VL53L0X_get_spad_info():
    write(_ADDRESS, b'\x80\x01')
    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x00\x00')

    write(_ADDRESS, b'\xff\x06')
    write(_ADDRESS, b'\x83')
    write(_ADDRESS, b'\x83' + ustruct.pack('B', read(_ADDRESS, 1)[0] | 0x04))
    write(_ADDRESS, b'\xff\x07')
    write(_ADDRESS, b'\x81\x01')

    write(_ADDRESS, b'\x80\x01')

    write(_ADDRESS, b'\x94\x6b')
    write(_ADDRESS, b'\x83\x00')

    _VL53L0X_start_timeout()
    write(_ADDRESS, b'\x83')
    while(read(_ADDRESS, 1) == b'\x00'):
        if(_VL53L0X_check_timeout_expired()):
            return 0, 0, False
        else:
            write(_ADDRESS, b'\x83')

    write(_ADDRESS, b'\x83\x01')
    write(_ADDRESS, b'\x92')
    tmp = read(_ADDRESS, 1)[0]

    count = tmp & 0x7f
    type_is_aperture = (tmp >> 7) & 0x01

    write(_ADDRESS, b'\x81\x00')
    write(_ADDRESS, b'\xff\x06')
    write(_ADDRESS, b'\x83')
    write(_ADDRESS, b'\x83' + ustruct.pack('B', read(_ADDRESS, 1)[0] & ~0x04))
    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x00\x01')

    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x80\x00')

    return count, type_is_aperture, True

# Check if timeout is enabled (set to nonzero value) and has expired
def _VL53L0X_check_timeout_expired():
    if(io_timeout > 0 and (utime.ticks_ms() - timeout_start) > io_timeout):
        return True
    return False

# Record the current time to check an upcoming timeout against
def _VL53L0X_start_timeout():
    global timeout_start
    timeout_start = utime.ticks_ms()


#SequenceStepEnables = {"tcc":0, "msrc":0, "dss":0, "pre_range":0, "final_range":0}
#SequenceStepTimeouts = {"pre_range_vcsel_period_pclks":0, "final_range_vcsel_period_pclks":0, "msrc_dss_tcc_mclks":0, "pre_range_mclks":0, "final_range_mclks":0, "msrc_dss_tcc_us":0, "pre_range_us":0, "final_range_us":0}


# Get the measurement timing budget in microseconds
# based on VL53L0X_get_measurement_timing_budget_micro_seconds()
# in us
def _VL53L0X_get_measurement_timing_budget():

    StartOverhead      = 1910 # note that this is different than the value in set_
    EndOverhead        = 960
    MsrcOverhead       = 660
    TccOverhead        = 590
    DssOverhead        = 690
    PreRangeOverhead   = 660
    FinalRangeOverhead = 550

    # "Start and end overhead times always present"
    budget_us = StartOverhead + EndOverhead

    enables = _VL53L0X_get_sequence_step_enables()
    timeouts = _VL53L0X_get_sequence_step_timeouts(enables["pre_range"])

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

    global measurement_timing_budget_us
    measurement_timing_budget_us = budget_us # store for internal reuse
    return budget_us

# Get sequence step enables
# based on VL53L0X_get_sequence_step_enables()
def _VL53L0X_get_sequence_step_enables():
    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG)
    sequence_config = read(_ADDRESS, 1)[0]
    SequenceStepEnables = {"tcc":0, "msrc":0, "dss":0, "pre_range":0, "final_range":0}
    SequenceStepEnables["tcc"]         = (sequence_config >> 4) & 0x1
    SequenceStepEnables["dss"]         = (sequence_config >> 3) & 0x1
    SequenceStepEnables["msrc"]        = (sequence_config >> 2) & 0x1
    SequenceStepEnables["pre_range"]   = (sequence_config >> 6) & 0x1
    SequenceStepEnables["final_range"] = (sequence_config >> 7) & 0x1
    return SequenceStepEnables

# Get sequence step timeouts
# based on get_sequence_step_timeout(),
# but gets all timeouts instead of just the requested one, and also stores
# intermediate values
def _VL53L0X_get_sequence_step_timeouts(pre_range):
    SequenceStepTimeouts = {"pre_range_vcsel_period_pclks":0, "final_range_vcsel_period_pclks":0, "msrc_dss_tcc_mclks":0, "pre_range_mclks":0, "final_range_mclks":0, "msrc_dss_tcc_us":0, "pre_range_us":0, "final_range_us":0}
    SequenceStepTimeouts["pre_range_vcsel_period_pclks"] = _VL53L0X_get_vcsel_pulse_period(__VL53L0X_VCSEL_PERIOD_RANGE_PRE)

    write(_ADDRESS, _MSRC_CONFIG_TIMEOUT_MACROP)
    SequenceStepTimeouts["msrc_dss_tcc_mclks"] = read(_ADDRESS, 1)[0] + 1
    SequenceStepTimeouts["msrc_dss_tcc_us"] = _VL53L0X_timeout_mclks_to_microseconds(SequenceStepTimeouts["msrc_dss_tcc_mclks"], SequenceStepTimeouts["pre_range_vcsel_period_pclks"])

    write(_ADDRESS, _PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI)
    SequenceStepTimeouts["pre_range_mclks"] = _VL53L0X_decode_timeout(ustruct.unpack('>H', read(_ADDRESS, 2)))
    SequenceStepTimeouts["pre_range_us"] = _VL53L0X_timeout_mclks_to_microseconds(SequenceStepTimeouts["pre_range_mclks"], SequenceStepTimeouts["pre_range_vcsel_period_pclks"])

    SequenceStepTimeouts["final_range_vcsel_period_pclks"] = _VL53L0X_get_vcsel_pulse_period(__VL53L0X_VCSEL_PERIOD_RANGE_FINAL)

    write(_ADDRESS, _FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI)
    SequenceStepTimeouts["final_range_mclks"] = _VL53L0X_decode_timeout(ustruct.unpack('>H', read(_ADDRESS, 2)))

    if (pre_range):
        SequenceStepTimeouts["final_range_mclks"] -= SequenceStepTimeouts["pre_range_mclks"]

    SequenceStepTimeouts["final_range_us"] = _VL53L0X_timeout_mclks_to_microseconds(SequenceStepTimeouts["final_range_mclks"], SequenceStepTimeouts["final_range_vcsel_period_pclks"])

    return SequenceStepTimeouts

# Decode VCSEL (vertical cavity surface emitting laser) pulse period in PCLKs
# from register value
# based on VL53L0X_decode_vcsel_period()
def _VL53L0X_decode_vcsel_period(reg_val):
    return (((reg_val) + 1) << 1)

# Get the VCSEL pulse period in PCLKs for the given period type.
# based on VL53L0X_get_vcsel_pulse_period()
def _VL53L0X_get_vcsel_pulse_period(type):
    if type == __VL53L0X_VCSEL_PERIOD_RANGE_PRE:
        write(_ADDRESS, _PRE_RANGE_CONFIG_VCSEL_PERIOD)
        return _VL53L0X_decode_vcsel_period(read(_ADDRESS, 1)[0])
    elif type == __VL53L0X_VCSEL_PERIOD_RANGE_FINAL:
        write(_ADDRESS, _FINAL_RANGE_CONFIG_VCSEL_PERIOD)
        return _VL53L0X_decode_vcsel_period(read(_ADDRESS, 1)[0])
    else:
        return 255

# Convert sequence step timeout from MCLKs to microseconds with given VCSEL period in PCLKs
# based on VL53L0X_calc_timeout_us()
def _VL53L0X_timeout_mclks_to_microseconds(timeout_period_mclks, vcsel_period_pclks):
    macro_period_ns = _VL53L0X_calc_macro_period(vcsel_period_pclks)
    return ((timeout_period_mclks * macro_period_ns) + (macro_period_ns / 2)) / 1000

# Calculate macro period in *nanoseconds* from VCSEL period in PCLKs
# based on VL53L0X_calc_macro_period_ps()
# PLL_period_ps = 1655; macro_period_vclks = 2304
def _VL53L0X_calc_macro_period(vcsel_period_pclks):
    return (((2304 * vcsel_period_pclks * 1655) + 500) / 1000)

# Decode sequence step timeout in MCLKs from register value
# based on VL53L0X_decode_timeout()
# Note: the original function returned a uint32_t, but the return value is
#always stored in a uint16_t.
def _VL53L0X_decode_timeout(reg_val):
    # format: "(LSByte * 2^MSByte) + 1"
    return ((reg_val & 0x00FF) << ((reg_val & 0xFF00) >> 8)) + 1;

# Set the measurement timing budget in microseconds, which is the time allowed
# for one measurement the ST API and this library take care of splitting the
# timing budget among the sub-steps in the ranging sequence. A longer timing
# budget allows for more accurate measurements. Increasing the budget by a
# factor of N decreases the range measurement standard deviation by a factor of
# sqrt(N). Defaults to about 33 milliseconds the minimum is 20 ms.
# based on VL53L0X_set_measurement_timing_budget_micro_seconds()
def _VL53L0X_set_measurement_timing_budget(budget_us):
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

    enables = _VL53L0X_get_sequence_step_enables()
    timeouts = _VL53L0X_get_sequence_step_timeouts(enables["pre_range"])

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

        final_range_timeout_mclks = _VL53L0X_timeout_microseconds_to_mclks(final_range_timeout_us, timeouts["final_range_vcsel_period_pclks"])

        if enables["pre_range"]:
            final_range_timeout_mclks += timeouts["pre_range_mclks"]

        encoded_timeout = _VL53L0X_encode_timeout(final_range_timeout_mclks)
        write(_ADDRESS, _FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI + ustruct.pack('BB', encoded_timeout >> 8 & 0xff, encoded_timeout & 0xff))

        # set_sequence_step_timeout() end
        global measurement_timing_budget_us
        measurement_timing_budget_us = budget_us # store for internal reuse
    return True

# Encode sequence step timeout register value from timeout in MCLKs
# based on VL53L0X_encode_timeout()
# Note: the original function took a uint16_t, but the argument passed to it
# is always a uint16_t.
def _VL53L0X_encode_timeout(timeout_mclks):
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
def _VL53L0X_timeout_microseconds_to_mclks(timeout_period_us, vcsel_period_pclks):
    macro_period_ns = _VL53L0X_calc_macro_period(vcsel_period_pclks)
    return (((timeout_period_us * 1000) + (macro_period_ns / 2)) / macro_period_ns)

# based on VL53L0X_perform_single_ref_calibration()
def _VL53L0X_perform_single_ref_calibration(vhv_init_byte):
    write(_ADDRESS, _SYSRANGE_START + ustruct.pack('B', 0x01 | vhv_init_byte)) # VL53L0X_REG_SYSRANGE_MODE_START_STOP

    _VL53L0X_start_timeout()
    write(_ADDRESS, _RESULT_INTERRUPT_STATUS)
    while (read(_ADDRESS, 1)[0] & 0x07) == 0:
        if _VL53L0X_check_timeout_expired():
            return False
        else:
            write(_ADDRESS, _RESULT_INTERRUPT_STATUS)

    write(_ADDRESS, _SYSTEM_INTERRUPT_CLEAR + b'\x01')
    write(_ADDRESS, _SYSRANGE_START + b'\x00')

    return True

def _VL53L0X_set_timeout(timeout):
    global io_timeout
    io_timeout = timeout

# Start continuous ranging measurements. If period_ms (optional) is 0 or not
# given, continuous back-to-back mode is used (the sensor takes measurements as
# often as possible) otherwise, continuous timed mode is used, with the given
# inter-measurement period in milliseconds determining how often the sensor
# takes a measurement.
# based on VL53L0X_StartMeasurement()
def VL53L0X_start_continuous(period_ms = 0):
    write(_ADDRESS, b'\x80\x01')
    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x00\x00')
    write(_ADDRESS, b'\x91' + ustruct.pack('B', stop_variable))
    write(_ADDRESS, b'\x00\x01')
    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x80\x00')

    if period_ms != 0:
        # continuous timed mode

        # VL53L0X_SetInterMeasurementPeriodMilliSeconds() begin
        write(_ADDRESS, _OSC_CALIBRATE_VAL)
        osc_calibrate_val = ustruct.unpack('>H', read(_ADDRESS, 2))[0]

        if osc_calibrate_val != 0:
            period_ms *= osc_calibrate_val

        write(_ADDRESS, _SYSTEM_INTERMEASUREMENT_PERIOD + ustruct.pack('>I', period_ms))

        # VL53L0X_SetInterMeasurementPeriodMilliSeconds() end

        write(_ADDRESS, _SYSRANGE_START + b'\x04') # VL53L0X_REG_SYSRANGE_MODE_TIMED
    else:
        # continuous back-to-back mode
        write(_ADDRESS, _SYSRANGE_START + b'\x02') # VL53L0X_REG_SYSRANGE_MODE_BACKTOBACK

# Returns a range reading in millimeters when continuous mode is active
# (read_range_single_millimeters() also calls this function after starting a
# single-shot range measurement)
def VL53L0X_read_range_continuous_millimeters():
    _VL53L0X_start_timeout()
    write(_ADDRESS, _RESULT_INTERRUPT_STATUS)
    while ((read(_ADDRESS, 1)[0] & 0x07) == 0):
        if _VL53L0X_check_timeout_expired():
            global did_timeout
            did_timeout = True
            raise OSError("read_range_continuous_millimeters timeout")
        else:
            write(_ADDRESS, _RESULT_INTERRUPT_STATUS)

    # assumptions: Linearity Corrective Gain is 1000 (default)
    # fractional ranging is not enabled
    write(_ADDRESS,  ustruct.pack('B', _RESULT_RANGE_STATUS[0] + 10))
    range = ustruct.unpack('>H', read(_ADDRESS, 2))

    write(_ADDRESS, _SYSTEM_INTERRUPT_CLEAR + b'\x01')

    return range

def VL53L0X_read_range_single_millimeters():
    write(_ADDRESS, b'\x80\x01')
    write(_ADDRESS, b'\xff\x01')
    write(_ADDRESS, b'\x00\x00')
    write(_ADDRESS, b'\x91' + ustruct.pack('B', stop_variable
    ))
    write(_ADDRESS, b'\x00\x01')
    write(_ADDRESS, b'\xff\x00')
    write(_ADDRESS, b'\x80\x00')

    write(_ADDRESS, _SYSRANGE_START + b'\x01')
    global did_timeout

    # "Wait until start bit has been cleared"
    _VL53L0X_start_timeout()
    write(_ADDRESS, _SYSRANGE_START)
    while (read(_ADDRESS, 1)[0] & 0x01):
        if _VL53L0X_check_timeout_expired():
            did_timeout = True
            raise OSError("read_range_single_millimeters timeout")
        else:
            write(_ADDRESS, _SYSRANGE_START)
    return VL53L0X_read_range_continuous_millimeters()

# Did a timeout occur in one of the read functions since the last call to
# timeout_occurred()?
def _VL53L0X_timeout_occurred():
    global did_timeout
    tmp = did_timeout
    did_timeout = False
    return tmp

# Set the VCSEL (vertical cavity surface emitting laser) pulse period for the
# given period type (pre-range or final range) to the given value in PCLKs.
# Longer periods seem to increase the potential range of the sensor.
# Valid values are (even numbers only):
#  pre:  12 to 18 (initialized default: 14)
#  final: 8 to 14 (initialized default: 10)
# based on VL53L0X_setVcselPulsePeriod()
def _VL53L0X_set_vcsel_pulse_period(type, period_pclks):
    vcsel_period_reg = _VL53L0X_encode_vcsel_period(period_pclks)

    enables = _VL53L0X_get_sequence_step_enables()
    timeouts = _VL53L0X_get_sequence_step_timeouts(enables["pre_range"])

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

    if type == __VL53L0X_VCSEL_PERIOD_RANGE_PRE:
        # "Set phase check limits"
        if period_pclks == 12:
            write(_ADDRESS, _PRE_RANGE_CONFIG_VALID_PHASE_HIGH + b'\x18')
        elif period_pclks == 14:
            write(_ADDRESS, _PRE_RANGE_CONFIG_VALID_PHASE_HIGH + b'\x30')
        elif period_pclks == 16:
            write(_ADDRESS, _PRE_RANGE_CONFIG_VALID_PHASE_HIGH + b'\x40')
        elif period_pclks == 18:
            write(_ADDRESS, _PRE_RANGE_CONFIG_VALID_PHASE_HIGH + b'\x50')
        else:
            return False

        write(_ADDRESS, _PRE_RANGE_CONFIG_VALID_PHASE_LOW + b'\x08')

        # apply new VCSEL period
        write(_ADDRESS, _PRE_RANGE_CONFIG_VCSEL_PERIOD + ustruct.pack('B', vcsel_period_reg))

        # update timeouts

        # set_sequence_step_timeout() begin
        # (SequenceStepId == VL53L0X_SEQUENCESTEP_PRE_RANGE)

        new_pre_range_timeout_mclks = _VL53L0X_timeout_microseconds_to_mclks(timeouts["pre_range_us"], period_pclks)

        encoded_timeout = _VL53L0X_encode_timeout(new_pre_range_timeout_mclks)
        write(_ADDRESS, _PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI + ustruct.pack('BB', encoded_timeout >> 8 & 0xff, encoded_timeout & 0xff))

        # set_sequence_step_timeout() end

        # set_sequence_step_timeout() begin
        # (SequenceStepId == VL53L0X_SEQUENCESTEP_MSRC)

        new_msrc_timeout_mclks = _VL53L0X_timeout_microseconds_to_mclks(timeouts["msrc_dss_tcc_us"], period_pclks)

        if new_msrc_timeout_mclks > 256:
            write(_ADDRESS, _MSRC_CONFIG_TIMEOUT_MACROP + b'\xff')
        else:
            write(_ADDRESS, _MSRC_CONFIG_TIMEOUT_MACROP + ustruct.pack('B', new_msrc_timeout_mclks - 1))

        # set_sequence_step_timeout() end
    elif type == __VL53L0X_VCSEL_PERIOD_RANGE_FINAL:
        if period_pclks == 8:
            write(_ADDRESS, _FINAL_RANGE_CONFIG_VALID_PHASE_HIGH + b'\x10')
            write(_ADDRESS, _FINAL_RANGE_CONFIG_VALID_PHASE_LOW + b'\x08')
            write(_ADDRESS, _GLOBAL_CONFIG_VCSEL_WIDTH + b'\x02')
            write(_ADDRESS, _ALGO_PHASECAL_CONFIG_TIMEOUT + b'\x0c')
            write(_ADDRESS, b'\xff\x01')
            write(_ADDRESS, _ALGO_PHASECAL_LIM + b'\x30')
            write(_ADDRESS, b'\xff\x00')
        elif period_pclks == 10:
            write(_ADDRESS, _FINAL_RANGE_CONFIG_VALID_PHASE_HIGH + b'\x28')
            write(_ADDRESS, _FINAL_RANGE_CONFIG_VALID_PHASE_LOW + b'\x08')
            write(_ADDRESS, _GLOBAL_CONFIG_VCSEL_WIDTH + b'\x03')
            write(_ADDRESS, _ALGO_PHASECAL_CONFIG_TIMEOUT + b'\x09')
            write(_ADDRESS, b'\xff\x01')
            write(_ADDRESS, _ALGO_PHASECAL_LIM + b'\x20')
            write(_ADDRESS, b'\xff\x00')
        elif period_pclks == 12:
            write(_ADDRESS, _FINAL_RANGE_CONFIG_VALID_PHASE_HIGH + b'\x38')
            write(_ADDRESS, _FINAL_RANGE_CONFIG_VALID_PHASE_LOW + b'\x08')
            write(_ADDRESS, _GLOBAL_CONFIG_VCSEL_WIDTH + b'\x03')
            write(_ADDRESS, _ALGO_PHASECAL_CONFIG_TIMEOUT + b'\x08')
            write(_ADDRESS, b'\xff\x01')
            write(_ADDRESS, _ALGO_PHASECAL_LIM + b'\x20')
            write(_ADDRESS, b'\xff\x00')
        elif period_pclks == 14:
            write(_ADDRESS, _FINAL_RANGE_CONFIG_VALID_PHASE_HIGH + b'\x48')
            write(_ADDRESS, _FINAL_RANGE_CONFIG_VALID_PHASE_LOW + b'\x08')
            write(_ADDRESS, _GLOBAL_CONFIG_VCSEL_WIDTH + b'\x03')
            write(_ADDRESS, _ALGO_PHASECAL_CONFIG_TIMEOUT + b'\x07')
            write(_ADDRESS, b'\xff\x01')
            write(_ADDRESS, _ALGO_PHASECAL_LIM + b'\x20')
            write(_ADDRESS, b'\xff\x00')
        else:
            # invalid period
            return False

        # apply new VCSEL period
        write(_ADDRESS, _FINAL_RANGE_CONFIG_VCSEL_PERIOD + ustruct.pack('B', vcsel_period_reg))

        # update timeouts

        # set_sequence_step_timeout() begin
        # (SequenceStepId == VL53L0X_SEQUENCESTEP_FINAL_RANGE)

        # "For the final range timeout, the pre-range timeout
        #  must be added. To do this both final and pre-range
        #  timeouts must be expressed in macro periods MClks
        #  because they have different vcsel periods."

        new_final_range_timeout_mclks = _VL53L0X_timeout_microseconds_to_mclks(timeouts["final_range_us"], period_pclks)

        if enables["pre_range"]:
            new_final_range_timeout_mclks += timeouts["pre_range_mclks"]

        encoded_timeout = _VL53L0X_encode_timeout(new_final_range_timeout_mclks)
        write(_ADDRESS, _FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI + ustruct.pack('BB', encoded_timeout >> 8 & 0xff, encoded_timeout & 0xff))

        # set_sequence_step_timeout end
    else:
        # invalid type
        return False

    # "Finally, the timing budget must be re-applied"

    _VL53L0X_set_measurement_timing_budget(measurement_timing_budget_us)

    # "Perform the phase calibration. This is needed after changing on vcsel period."
    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG)
    sequence_config = read(_ADDRESS, 1)
    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG + b'\x02')
    _VL53L0X_perform_single_ref_calibration(0x0)
    write(_ADDRESS, _SYSTEM_SEQUENCE_CONFIG + sequence_config)

    return True

# Encode VCSEL pulse period register value from period in PCLKs
# based on VL53L0X_encode_vcsel_period()
def _VL53L0X_encode_vcsel_period(period_pclks):
    return((period_pclks >> 1) - 1)

VL53L0X_init()
VL53L0X_start_continuous()
VL53L0X_read_range_continuous_millimeters()