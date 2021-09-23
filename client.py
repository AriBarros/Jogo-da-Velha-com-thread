import  pygame
import os,sys
from grid_multi import Grid
import socket
import threading

def create_thread(target):
    thread=threading.Thread(target=target)
    thread.daemon=True
    thread.start()


pygame.init()
HOST='127.0.0.1'
PORT=9009

connection_established=False
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sock.connect((HOST,PORT))
    connection_established=True
except :
    pass



surface=pygame.display.set_mode((600,630))
pygame.display.set_caption('Jogo da Velha')

grid=Grid()
starting=True
player="O"
turn=False
playing="True"

def receive_data():
    global turn,connection_established
    while True:
        try:
            data=sock.recv(1024).decode()
            data=data.split('-')
            x,y=int(data[0]),int(data[1])
            if data[2]=='Yourturn':
                turn=True
            if data[3] =="False":
                grid.game_over=True
            while playing!="True":
                pass        
            if grid.get_cell_value(x,y)==0:
                grid.set_cell_value(x,y,"X")
        except :
            print('Conexao remota encerrada')
            grid.clear_grid()
            connection_established=False
            grid.game_over=True
            break

create_thread(receive_data)

def status_bar():
    font = pygame.font.Font('assets/04b19.ttf', 16)
    if not connection_established:
        whoturn ="Nao conectado com o oponente - exit(sair)"
    elif grid.game_over:
        if grid.winner !=0:
            whoturn= " Ganhador = " + player + " | pressione espaco para limpar "
        else:
            whoturn="Game over | pressione espaco para limpar"
    elif turn==True:
        whoturn="Seu turno" 
    else:
        whoturn="Turno do oponente"    
    text = font.render(f'Player O |  {whoturn}', True, (0,100,0),) 
    textRect = text.get_rect() 
    textRect.center = (300, 615)
    surface.blit(text, textRect)


while starting:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            starting=False
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellx,celly=pos[0]//200,pos[1]//200
                    grid.set_mouse_input(cellx,celly,player)
                    if grid.game_over:
                        playing="False"
                    send_data='{}-{}-{}-{}'.format(cellx,celly,'Yourturn',playing).encode()
                    sock.send(send_data)
                    turn=False

            if grid.game_over:
                print("Game over")

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over=False
                playing="True"
                print("Recomecar")
                if not connection_established:
                    grig.game_over=True

            elif event.key ==pygame.K_ESCAPE:
                starting=False

    surface.fill((255,160,122))
    grid.draw(surface)
    status_bar()    
    pygame.display.flip()