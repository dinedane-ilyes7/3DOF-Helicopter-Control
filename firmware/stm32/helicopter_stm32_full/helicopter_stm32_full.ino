#include "Arduino.h"

// ============================================================
// YOUR ORIGINAL DEFINITIONS — UNTOUCHED
// ============================================================
#define JOY_X PB0
#define JOY_Y PB1

int joyX = 0;
int joyY = 0;

float pitch_angle     = 0;
float elevation_angle = 0;
float travel_angle    = 0;

// ============================================================
// PWM reception + output state
// ============================================================
static volatile uint16_t g_pwm1_us = 1000;
static volatile uint16_t g_pwm2_us = 1000;

static char    rx_buf[32];
static uint8_t rx_idx = 0;

// ============================================================
// NON-BLOCKING TIMING
// Replaces safeRegisterDelay(50) in loop()
// Uses TIM5 as a free-running microsecond counter
// ============================================================
static uint32_t last_sensor_us = 0;  // last time we sent sensor data
#define SENSOR_INTERVAL_US  50000    // send sensors data every 50ms = 20Hz

void setupTIM5_micros()
{
    RCC->APB1ENR |= RCC_APB1ENR_TIM5EN;
    TIM5->PSC  = 167;    // 168MHz / 168 = 1MHz -> 1us per tick
    TIM5->ARR  = 0xFFFFFFFF;  // 32-bit free-running counter
    TIM5->CNT  = 0;
    TIM5->CR1 |= TIM_CR1_CEN;
}

inline uint32_t micros_now()
{
    return TIM5->CNT;
}

// ============================================================
// YOUR ORIGINAL FUNCTIONS — UNTOUCHED
// ============================================================
void safeRegisterDelay(uint32_t ms) {
    volatile uint32_t count = ms * 16500;
    while (count--) { __asm__("nop"); }
}

void setupEncoderPins()
{
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIODEN;

    /* PA1 -> TIM2_CH2 */
    GPIOA->MODER &= ~(3U << (1*2)); GPIOA->MODER |= (2U << (1*2));
    GPIOA->PUPDR &= ~(3U << (1*2)); GPIOA->PUPDR |= (1U << (1*2));
    GPIOA->AFR[0] &= ~(0xF << (1*4)); GPIOA->AFR[0] |= (1U << (1*4));

    /* PA5 -> TIM2_CH1 */
    GPIOA->MODER &= ~(3U << (5*2)); GPIOA->MODER |= (2U << (5*2));
    GPIOA->PUPDR &= ~(3U << (5*2)); GPIOA->PUPDR |= (1U << (5*2));
    GPIOA->AFR[0] &= ~(0xF << (5*4)); GPIOA->AFR[0] |= (1U << (5*4));

    /* PA6 -> TIM3_CH1 */
    GPIOA->MODER &= ~(3U << (6*2)); GPIOA->MODER |= (2U << (6*2));
    GPIOA->PUPDR &= ~(3U << (6*2)); GPIOA->PUPDR |= (1U << (6*2));
    GPIOA->AFR[0] &= ~(0xF << (6*4)); GPIOA->AFR[0] |= (2U << (6*4));

    /* PA7 -> TIM3_CH2 */
    GPIOA->MODER &= ~(3U << (7*2)); GPIOA->MODER |= (2U << (7*2));
    GPIOA->PUPDR &= ~(3U << (7*2)); GPIOA->PUPDR |= (1U << (7*2));
    GPIOA->AFR[0] &= ~(0xF << (7*4)); GPIOA->AFR[0] |= (2U << (7*4));

    /* PD12 -> TIM4_CH1 */
    GPIOD->MODER &= ~(3U << (12*2)); GPIOD->MODER |= (2U << (12*2));
    GPIOD->PUPDR &= ~(3U << (12*2)); GPIOD->PUPDR |= (1U << (12*2));
    GPIOD->AFR[1] &= ~(0xF << ((12-8)*4)); GPIOD->AFR[1] |= (2U << ((12-8)*4));

    /* PD13 -> TIM4_CH2 */
    GPIOD->MODER &= ~(3U << (13*2)); GPIOD->MODER |= (2U << (13*2));
    GPIOD->PUPDR &= ~(3U << (13*2)); GPIOD->PUPDR |= (1U << (13*2));
    GPIOD->AFR[1] &= ~(0xF << ((13-8)*4)); GPIOD->AFR[1] |= (2U << ((13-8)*4));
}

void setupEncoder(TIM_TypeDef* TIMx)
{
    TIMx->CR1   &= ~TIM_CR1_CEN;
    TIMx->DIER  &= ~TIM_DIER_UIE;
    TIMx->SMCR  = TIM_SMCR_SMS_0 | TIM_SMCR_SMS_1;
    TIMx->CCMR1 = TIM_CCMR1_CC1S_0 | TIM_CCMR1_CC2S_0;
    TIMx->CCER  = TIM_CCER_CC1E | TIM_CCER_CC2E;
    TIMx->ARR   = 65535;
    TIMx->CNT   = 32767;
    TIMx->SR    = 0;
    TIMx->CR1  |= TIM_CR1_CEN;
}

void setupDirectUSART2()
{
    RCC->APB1ENR |= RCC_APB1ENR_USART2EN;
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

    GPIOA->MODER &= ~((3U << (2*2)) | (3U << (3*2)));
    GPIOA->MODER |=  ((2U << (2*2)) | (2U << (3*2)));
    GPIOA->AFR[0] &= ~((0xFU << (2*4)) | (0xFU << (3*4)));
    GPIOA->AFR[0] |=  ((7U  << (2*4)) | (7U  << (3*4)));

    USART2->BRR = 0x16D;
    USART2->CR1 = USART_CR1_UE | USART_CR1_TE | USART_CR1_RE;
}

void transmitChar(char c) {
    while (!(USART2->SR & USART_SR_TXE));
    USART2->DR = (c & 0xFF);
}

void printStr(const char* str) {
    while(*str) transmitChar(*str++);
}

void printFloat(float val, int decimals) {
    if (val < 0) { transmitChar('-'); val = -val; }
    long intPart = (long)val;
    char buf[12];
    int i = 0;
    if (intPart == 0) buf[i++] = '0';
    while (intPart > 0) { buf[i++] = (intPart % 10) + '0'; intPart /= 10; }
    while (i > 0) transmitChar(buf[--i]);
    transmitChar('.');
    val -= (long)val;
    for (int d = 0; d < decimals; d++) {
        val *= 10;
        int digit = (int)val;
        transmitChar(digit + '0');
        val -= digit;
    }
}

// ============================================================
// TIM1 — 50Hz RC PWM on PA8 (CH1) and PA10 (CH3)
// ============================================================
void setupPWMOutput()
{
    RCC->APB2ENR |= RCC_APB2ENR_TIM1EN;
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

    GPIOA->MODER  &= ~((3U << (8*2))  | (3U << (10*2)));
    GPIOA->MODER  |=  ((2U << (8*2))  | (2U << (10*2)));
    GPIOA->OTYPER &= ~((1U << 8)      | (1U << 10));
    GPIOA->OSPEEDR|=  ((3U << (8*2))  | (3U << (10*2)));
    GPIOA->PUPDR  &= ~((3U << (8*2))  | (3U << (10*2)));

    GPIOA->AFR[1] &= ~((0xFU << ((8-8)*4)) | (0xFU << ((10-8)*4)));
    GPIOA->AFR[1] |=  ((1U   << ((8-8)*4)) | (1U   << ((10-8)*4)));

    TIM1->CR1   = 0;
    TIM1->DIER  = 0;
    TIM1->PSC   = 167;     // 168MHz / 168 = 1MHz -> 1us per tick
    TIM1->ARR   = 19999;   // 20ms = 50Hz

    TIM1->CCMR1 &= ~(TIM_CCMR1_OC1M | TIM_CCMR1_CC1S);
    TIM1->CCMR1 |=  (TIM_CCMR1_OC1M_1 | TIM_CCMR1_OC1M_2 | TIM_CCMR1_OC1PE);

    TIM1->CCMR2 &= ~(TIM_CCMR2_OC3M | TIM_CCMR2_CC3S);
    TIM1->CCMR2 |=  (TIM_CCMR2_OC3M_1 | TIM_CCMR2_OC3M_2 | TIM_CCMR2_OC3PE);

    TIM1->CCER  |=  (TIM_CCER_CC1E | TIM_CCER_CC3E);
    TIM1->CCR1   = 1000;
    TIM1->CCR3   = 1000;
    TIM1->BDTR  |= TIM_BDTR_MOE;
    TIM1->EGR    = TIM_EGR_UG;
    TIM1->SR     = 0;
    TIM1->CR1   |= TIM_CR1_CEN;
}

// ============================================================
// ESC ARMING — blocking is OK here, happens once at boot only
// ============================================================
void armESCs()
{
    TIM1->CCR1 = 1000;
    TIM1->CCR3 = 1000;
    safeRegisterDelay(4000);
    safeRegisterDelay(200);
}

// ============================================================
// NON-BLOCKING RX PARSER — drains every byte waiting in USART2
// Called every loop iteration — never blocks
// ============================================================
void parsePWMInput()
{
    while (USART2->SR & USART_SR_RXNE)
    {
        char c = (char)(USART2->DR & 0xFF);

        if (c == '\n')
        {
            rx_buf[rx_idx] = '\0';

            uint8_t comma_pos = 0;
            for (uint8_t i = 0; i < rx_idx; i++) {
                if (rx_buf[i] == ',') { comma_pos = i; break; }
            }

            if (comma_pos > 0)
            {
                uint16_t v1 = 0, v2 = 0;
                for (uint8_t i = 0; i < comma_pos; i++) {
                    if (rx_buf[i] >= '0' && rx_buf[i] <= '9')
                        v1 = v1 * 10 + (rx_buf[i] - '0');
                }
                for (uint8_t i = comma_pos + 1; i < rx_idx; i++) {
                    char ch = rx_buf[i];
                    if (ch == '\r') break;
                    if (ch >= '0' && ch <= '9')
                        v2 = v2 * 10 + (ch - '0');
                }

                // Safety clamp
                if (v1 >= 1000 && v1 <= 1700) TIM1->CCR1 = v1;
                if (v2 >= 1000 && v2 <= 1700) TIM1->CCR3 = v2;
            }

            rx_idx = 0;
        }
        else if (c != '\r')
        {
            if (rx_idx < sizeof(rx_buf) - 1)
                rx_buf[rx_idx++] = c;
            else
                rx_idx = 0;  // overflow guard — flush corrupt frame
        }
    }
}

// ============================================================
// SENSOR TRANSMIT — sends one line of sensor data
// Only called when 50ms has elapsed (non-blocking)
// ============================================================
void sendSensorData()
{
    int pitch_count     = (int16_t)(TIM2->CNT - 32767);
    int elevation_count = (int16_t)(TIM3->CNT - 32767);
    int travel_count    = (int16_t)(TIM4->CNT - 32767);

    pitch_angle     = (pitch_count     * 360.0f) / 4000.0f;
    elevation_angle = (elevation_count * 360.0f) / 4000.0f;
    travel_angle    = (travel_count    * 360.0f) / 4000.0f;

    joyX = analogRead(JOY_X);
    joyY = analogRead(JOY_Y);

    float joyX_volt = joyX * (3.3f / 4095.0f);
    float joyY_volt = joyY * (3.3f / 4095.0f);

    printFloat(pitch_angle, 2);     printStr(",");
    printFloat(travel_angle, 2);    printStr(",");
    printFloat(elevation_angle, 2); printStr(",");
    printFloat(joyY_volt, 2);       printStr(",");
    printFloat(joyX_volt, 2);       printStr("\r\n");
}

// ============================================================
// setup()
// ============================================================
void setup()
{
    __disable_irq();

    pinMode(JOY_X, INPUT_ANALOG);
    pinMode(JOY_Y, INPUT_ANALOG);

    setupEncoderPins();

    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;
    RCC->APB1ENR |= RCC_APB1ENR_TIM3EN;
    RCC->APB1ENR |= RCC_APB1ENR_TIM4EN;

    setupEncoder(TIM2);
    setupEncoder(TIM3);
    setupEncoder(TIM4);

    setupDirectUSART2();

    __enable_irq();

    safeRegisterDelay(500);

    setupPWMOutput();
    setupTIM5_micros();   // free-running microsecond counter
    armESCs();            // blocks once for 4s — ESCs arm silently

    last_sensor_us = micros_now();
}

// ============================================================
// loop() — now fully non-blocking
// Runs as fast as possible:
//   - parsePWMInput() drains RX buffer every iteration
//   - sendSensorData() fires only every 50ms via timer check
// No delays, no blocking — RX buffer never overflows
// ============================================================
void loop()
{
    // 1. Always drain RX first — highest priority
    parsePWMInput();

    // 2. Send sensor data every 50ms non-blocking
    uint32_t now = micros_now();
    if ((now - last_sensor_us) >= SENSOR_INTERVAL_US)
    {
        last_sensor_us = now;
        sendSensorData();
    }
}
