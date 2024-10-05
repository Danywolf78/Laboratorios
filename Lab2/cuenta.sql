create database cuentas;
use cuentas ;
create table cuentabancaria (
Dni char(8) primary key,
Nombre varchar(50) not null,
Apellido varchar(50) not null,
Edad INT not null,
Saldo FLoat not null
) ;
create table cuentabancariaahorro(
Dni  char(8),
Intereses_Mensuales float not null,
foreign key  ( Dni) references cuentas(Dni)  -- Relacion con cuentabancaria
);
create table cuentabancariacorriente(
Dni  char(8),
Descubierto float not null,
foreign key  ( Dni) references cuentas(Dni) -- Relacion con cuentabancaria
);


