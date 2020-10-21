%input P1dB compression point
%all power measured in dB

clear;
clc;

%start of the model

Pin = 1:0.001:40; % input power
A = 200; % saturated output level
r = 10; % nonlinearity
gain = 5;% the gain of this amplifier
Po = (Pin+gain)./((1+(Pin+gain)/A).^(2*r)).^(1/(2*r)); % a SSPA model
Po_ideal = Pin+gain; % ideal output
%end of the model

%in reality, instead of using this model, we will measure the power in and 
%power out, calculate the delta, then store them in
%a index. We pick out the index that contains delta that is closest to 1,
%that Pin(index) would be the point that is closest to P1dB compression point


plot(Pin, Po_ideal);
hold on;
plot(Pin, Po);

ylim([0 45])
xlabel('Pin(dB)');
ylabel('Po(dB)');
grid on;


% algorithm used to find P1dB compression point
Pdelta = Po_ideal - Po; % find delta
[bincounts,ind] = histc(1,Pdelta); % find the index that contains closest delta to 1dB
%Pin(ind) is Pin when Po is 1dB lower than expected
plot(Pin(ind),Po(ind),'r*')
legend('ideal','Po','1dB compression point');

fprintf('input P1dB compression point is %5.4f dB\n',Pin(ind))
fprintf('at which point output power is %5.4f dB\n',Po(ind))
