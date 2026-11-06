
#include <Servo.h>

Servo myServo;

const int SERVO_PIN = 9;

const int REST_POSITION = 0;
const int JUMP_POSITION = 90;

const unsigned long JUMP_HOLD_TIME = 150;
const unsigned long RETURN_TIME = 150;

enum ServoState {
  IDLE,
  JUMPING,
  RETURNING
};

ServoState currentState = IDLE;

unsigned long previousTime = 0;

void setup() {

  Serial.begin(9600);

  myServo.attach(SERVO_PIN);

  myServo.write(REST_POSITION);

  Serial.println("Arduino Ready!");
}

void loop() {

  if (Serial.available() > 0) {

    char command = Serial.read();

    if (command == 'J' && currentState == IDLE) {

      myServo.write(JUMP_POSITION);

      previousTime = millis();

      currentState = JUMPING;

      Serial.println("JUMP STARTED!");
    }
  }

  unsigned long currentTime = millis();

  if (
    currentState == JUMPING &&
    currentTime - previousTime >= JUMP_HOLD_TIME
  ) {

    myServo.write(REST_POSITION);

    previousTime = currentTime;

    currentState = RETURNING;
  }

  if (
    currentState == RETURNING &&
    currentTime - previousTime >= RETURN_TIME
  ) {

    currentState = IDLE;

    Serial.println("JUMP COMPLETED!");
  }
}
