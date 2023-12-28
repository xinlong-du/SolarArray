clear;clc;
%B=50
A=737.2881;
Iy=239796.0797;
Iz=1123859.5690;
Iw=518574174.1068;
J=3010.5929;
y0=0.0000;
z0=-39.5459;
E=200000;
nu=0.3;
G=E/(2*(1+nu));
L=6669;

r2squ=(Iy+Iz)/A+y0*y0+z0*z0;
r0squ=(Iy+Iz)/A;

Nz=pi^2*E*Iz/(L^2);
%Ny=pi^2*E*Iy/(L^2);

NxW=(G*J+pi^2*E*Iw/(L^2))/r2squ;
Nx=(G*J)/r2squ;

NcrW=(NxW+Nz-sqrt((NxW+Nz)^2-4*NxW*Nz*r0squ/(r0squ+z0^2)))/2/r0squ*(r0squ+z0^2)
Ncr=(Nx+Nz-sqrt((Nx+Nz)^2-4*Nx*Nz*r0squ/(r0squ+z0^2)))/2/r0squ*(r0squ+z0^2)

NcrLTBw=sqrt((pi^2*E*Iy/L^2)*(G*J+pi^2*E*Iw/L^2))/(4448.2216*25.4)
NcrLTB =sqrt((pi^2*E*Iy/L^2)*(G*J))/(4448.2216*25.4)
errLTB=(NcrLTBw-NcrLTB)/NcrLTBw