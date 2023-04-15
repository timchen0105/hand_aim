#include<Mouse.h>

int pre_x = 0;
int pre_y = 0;
int x = 0;
int y = 0;
int diff_x = 0;
int diff_y = 0;
int isFire = 0;

void setup()
{
	Serial.begin(9600);
    Mouse.begin();
}

void loop()
{   
    if(Serial.available()){
        x = Serial.parseInt();
        y = Serial.parseInt();
        isFire = Serial.parseInt();
        
        diff_x = x - pre_x;
        diff_y = y - pre_y;

        Mouse.move(diff_x, diff_y, 0);
        if(isFire == 1){
            Mouse.click(MOUSE_LEFT);
        }

        pre_x = x;
        pre_y = y;
    }
}
