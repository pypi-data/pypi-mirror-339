import os

restaurantes = [{'nome':'Bolinho', 'categoria': 'Doces','ativo':False}, {'nome':'Pizza legal', 'categoria':'Pizza', 'ativo':True}, {'nome':'Praça', 'categoria': 'Japonesa','ativo':False}]
#.              0.        1. 
#.              ativo.    desativado 
def exibir_nome_do_programa():
 print (""""
🇸​​​​​🇦​​​​​🇧​​​​​🇴​​​​​🇷​​​​​ 🇪​​​​​🇽​​​​​🇵​​​​​🇷​​​​​🇪​​​​​🇸​​​​​🇸​​​​​
""")

def exibir_menu_principal():
  print('1. Cadastrar restaurante')
  print('2. Listar restaurantes')
  print('3. Ativar restaurante')
  print('4. Sair')

def finalizar_app():
  os.system('clear')
  print('Finalizando o app\n')
# isso asssima é uma função/bloco de codigo para realizar uma função.

def opcao_invalida():
  print('Opção inválida!')
  input('Digite uma tecla para voltar ao menu principal')
  main()

def cadastrar_novo_restaurante():
  os.system('clear')
  print('Cadastro e novos restaurantes\n')
  nome_do_restaurante = input('Digite o nome do retaurante que deseja cadastrar: ')
  categoria = input(f'Digite o nome da categoria do restaurante {nome_do_restaurante}: ')
  dados_do_restaurante = {'nome':nome_do_restaurante,'categoria':categoria, 'ativo':False}  
  restaurantes.append(dados_do_restaurante)
  print(f'O restaurante {nome_do_restaurante} foi cadastrasdo com suceso')
  input('\nDigite uma tecla para votar ao menu principal')
  main()

def listar_restaurantes():
  os.system('clear')
  print('Listar restaurantes\n')
  
  for restaurante in restaurantes:
    nome_restaurante = restaurante['nome']
    categoria = restaurante['categoria']
    ativo = restaurante['ativo']
    print(f'-{nome_restaurante} | {categoria} | {ativo}')
#para cada restaurante na lista de restaurantes: nome 
  
  input('\nDigite uma tecla para voltar ao menu principal')
  main()

def alternar_status_restaurante():
  exibir_subtitulo('Alternando estado do restaurante')
  nome_restaurante = input('Digite o nome do restaurante que deseja alternar o estado: ')
  restaurante_enontrado = False 

  for restaurante in restaurantes:
    if nome_restaurante == restaurante['nome']:
      restaurante_enontrado = True
      restaurante['ativo'] = not restaurante['ativo']
      mensagem = f'O restaurante {nome_restaurante} foi ativado com sucesso' if restaurante['ativo'] else f'O restaurante {nome_restaurante} foi desativado com sucesso'
      print(mensagem)
  if not restaurante_enontrado: 
    print('O restaurante não foi encontrado')
  
  input('\nDigite uma tecla para voltar ao menu principal')
  main()

def escolher_opcao():
  try:
     opcao_escolhida = int(input('Escolha uma opção: '))
# opcao_esolhida = int(opcao_escolhida)

     if opcao_escolhida == 1:
      cadastrar_novo_restaurante()
     elif opcao_escolhida == 2:
      listar_restaurantes()
     elif opcao_escolhida == 3:
      alternar_status_restaurante()
     elif opcao_escolhida ==4:
       finalizar_app() 
     else:
       opcao_invalida()
  except:
    opcao_invalida()

def main():
  os.system('clear')
  exibir_nome_do_programa()
  exibir_menu_principal()
  escolher_opcao()
  
if __name__ == '__main__':
  main()