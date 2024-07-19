from tabulate import tabulate
import numpy as np

resultado = np.array([(1, '2024-04-14', 1884.28, 1884.28, 0.0, 77, 0, 77, 'Casa Grande', 'Campo Emilly Ribeiro, 91', '+55 01 99932 6855', 'bbrito@example.net', 616), (2, '2022-05-08', 2786.56, 2786.56, 0.0, 23, 0, 23, 'Moura e Filhos', 'Largo Henry Gabriel Lima, 558', '+55 (58) 9 5530 6806', 'carlos-eduardopastor@example.org', 597), (3, '2023-09-25', 1726.72, 1726.72, 0.0, 17, 0, 17, 'Correia Cirino S.A.', 'Loteamento Enzo Gabriel Guerra, 2', '+55 (39) 9 1771 9851', 'sophiemarques@example.net', 1030), (4, '2020-07-28', 4508.06, 4508.06, 0.0, 87, 0, 87, 'Barros Ltda.', 'Fazenda de Moreira, 12', '+55 (084) 93890-7567', 'garciaclara@example.com', 1097), (5, '2020-12-02', 1786.64, 1786.64, 0.0, 77, 0, 77, 'Casa Grande', 'Campo Emilly Ribeiro, 91', '+55 01 99932 6855', 'bbrito@example.net', 616), (6, '2023-04-13', 3387.49, 3387.49, 0.0, 10, 0, 10, 'Marques Vieira - ME', 'Esplanada Macedo, 345', '+55 (62) 95766-3059', 'mendoncatheodoro@example.net', 1052), (7, '2021-09-01', 903.0, 903.0, 0.0, 79, 0, 79, 'Novais Fogaça S.A.', 'Jardim Agatha Monteiro, 943', '+55 (27) 9 8723-6242', 'da-conceicaomaite@example.com', 956), (8, '2020-06-18', 237.84, 237.84, 0.0, 12, 0, 12, 'Moraes', 'Praça Sá, 2', '+55 53 94710 7667', 'macedojuliana@example.com', 692), (9, '2021-01-02', 2340.06, 2340.06, 0.0, 37, 0, 37, 'Costela', 'Vereda Santos, 27', '+55 (031) 97936-8421', 'bella20@example.org', 908), (10, '2021-02-14', 5451.24, 5451.24, 0.0, 17, 0, 17, 'Correia Cirino S.A.', 'Loteamento Enzo Gabriel Guerra, 2', '+55 (39) 9 1771 9851', 'sophiemarques@example.net', 1030), (11, '2020-08-04', 5336.46, 5336.46, 0.0, 49, 0, 49, 'Costela S.A.', 'Lago de Moreira, 18', '+55 (24) 98989 7965', 'luiz-otavioduarte@example.com', 968), (12, '2021-07-13', 3906.5, 3906.5, 0.0, 84, 0, 84, 'Dias Lima - ME', 'Praça de Sampaio, 369', '+55 31 97537 7140', 'carvalhojade@example.net', 935), (13, '2023-04-23', 5555.05, 5555.05, 0.0, 52, 0, 52, 'Vieira - ME', 'Lago Cavalcanti, 5', '+55 88 9 2195-6760', 'martinsbreno@example.com', 1041), (14, '2022-09-13', 1568.31, 1568.31, 0.0, 52, 0, 52, 'Vieira - ME', 'Lago Cavalcanti, 5', '+55 88 9 2195-6760', 'martinsbreno@example.com', 1041)])
#
#(1, '2024-04-14', 1884.28, 1884.28, 0.0, 77, 0, 77, 'Casa Grande', 'Campo Emilly Ribeiro, 91', '+55 01 99932 6855', 'bbrito@example.net', 616)
#
nova = np.delete(resultado,np.r_[5:7, 9:13], axis=1)

print(tabulate(tabular_data=nova,  headers=["ID","Data Compra", "Valor Total", "Valor Pago", "Valor Desconto", "ID F", "Fornecedor"]))
