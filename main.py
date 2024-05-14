import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
import random

class GameState:
    def __init__(self):
        self.num_jogadores = 0
        self.jogadores = []
        self.classes_label = Label()
        self.valores_classe = {
            "Tank": (1000, 10),
            "Assassino": (200, 45),
            "Feiticeiro": (300, 40),
            "Atirador": (400, 35),
            "Curandeiro": (500, -50),
        }
        self.inimigo = None

    def definir_numero_jogadores(self, num_jogadores):
        self.num_jogadores = num_jogadores

    def reset(self):
        self.num_jogadores = 0
        self.jogadores = []
        self.inimigo = None

    def criar_inimigo(self):
        self.inimigo = Personagem(nome="Inimigo", classe="Inimigo", derrotado=1)
        self.atualizar_status_inimigo()

    def atualizar_status_inimigo(self):
        if self.inimigo.vida <=0:
            self.inimigo.vida = 500 + 100 * self.num_jogadores * self.inimigo.derrotado
            self.inimigo.dano = 30 + self.num_jogadores * 10 + self.inimigo.derrotado * 5
        else:
            self.inimigo.vida = 500 + 100 * self.num_jogadores * self.inimigo.derrotado
            self.inimigo.dano = 30 + self.num_jogadores * 10 + self.inimigo.derrotado * 5

    def print_game_state(self):
        print("Número de Jogadores:", self.num_jogadores)
        print("Jogadores:")
        for i, jogador in enumerate(self.jogadores):
            print(f"Posição na lista: {i}, Nome: {jogador.nome}, Classe: {jogador.classe}, Vida: {jogador.vida}, Dano: {jogador.dano}")
        print("Inimigo:")
        if self.inimigo:
            print(f"Nome: {self.inimigo.nome}, Derrota: {self.inimigo.derrotado}, Vida: {self.inimigo.vida}, Dano: {self.inimigo.dano}")
    
    def display_situacao(self):
        text = ""
        for jogador in self.jogadores:
            text += f"{jogador.classe} tem {jogador.vida} de vida e {jogador.dano} de dano\n"
        self.classes_label.text = text
        self.classes_label.halign = 'center'       

class Personagem:
    def __init__(self, nome, classe, vida=None, dano=None, derrotado=0):
        self.nome = nome
        self.classe = classe
        self.vida, self.dano = self.definir_valores(classe)
        self.derrotado = derrotado
        print(f"Criando personagem {self.nome} da classe {self.classe} com vida {self.vida} e dano {self.dano}")

    def definir_valores(self, classe):
        valores = game_state.valores_classe.get(classe, (0, 0))
        print(f"Valores para classe {classe}: {valores}")
        return valores

game_state = GameState()

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10)       

        label1 = Label(text="RPGTxt\n", font_size=50, halign='center')
        label2 = Label(text="\nBem-vindo à aventura na Caverna do Mistério!\nVocê está pronto para explorar seus segredos?\n", halign='center')
        button = Button(text='Iniciar Jogo', font_size=40 , size_hint_y=None, height='100dp')
        label3 = Label(text="\nHudsaw\nbeta\n", halign='center')
        button.bind(on_press=self.iniciar_jogo)
        
        layout.add_widget(label1)
        layout.add_widget(label2)
        layout.add_widget(button)
        layout.add_widget(label3)

        self.add_widget(layout)

    def iniciar_jogo(self, instance):
        print("O usuário inicou o jogo!")
        
        game_state.reset() 
        app.root.current = "num_jogadores"

class NumJogadoresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=10)

        label = Label(text="Selecione o número de jogadores:", font_size=20)
        self.layout.add_widget(label)

        for i in range(1, 6):
            button = Button(text=str(i), size_hint=(1, None), height=50)
            button.bind(on_press=self.on_select_players)
            self.layout.add_widget(button)

        self.add_widget(self.layout)

    def on_select_players(self, instance):
        num_jogadores_escolhido = int(instance.text)
        print(f"Número de jogadores escolhido: {num_jogadores_escolhido}")
        game_state.num_jogadores = num_jogadores_escolhido
        app.root.get_screen("classe_selection").update_classes_layout(game_state.num_jogadores)
        app.root.current = "classe_selection"

class ClasseSelectionScreen(Screen):
    def __init__(self, num_jogadores, **kwargs):
        super().__init__(**kwargs)
        self.num_jogadores = 0
        self.layout = GridLayout(cols=1, spacing=10)
        self.classes_disponiveis = ["Tank", "Assassino", "Feiticeiro", "Atirador", "Curandeiro"]
        self.botao_classes = []
        self.classes_jogadores = []

        self.add_widget(self.layout)

    def update_classes_layout(self, num_jogadores):
        self.num_jogadores = num_jogadores
        self.layout.clear_widgets() 
        for i in range(self.num_jogadores):
            jogador_label = Label(text=f"Jogador {i+1}: Escolha sua classe para a jornada:")
            self.layout.add_widget(jogador_label)
            jogador_layout = GridLayout(cols=len(self.classes_disponiveis), spacing=10)
            for classe in self.classes_disponiveis:
                button = Button(text=classe, size_hint=(None, None), size=(150, 50))
                button.bind(on_press=self.on_select_class)
                button.jogador_index = i + 1
                jogador_layout.add_widget(button)
                self.botao_classes.append(button)
            self.layout.add_widget(jogador_layout)

    def on_select_class(self, instance):
        jogador_index = instance.jogador_index
        escolha = instance.text
        print(f"Jogador {jogador_index} escolheu a classe: {escolha}")

        jogador = Personagem(nome=f"Jogador {jogador_index}", classe=escolha)
        game_state.jogadores.append(jogador)  # Adiciona o jogador à lista de jogadores

        instance.background_color = get_color_from_hex("#FF0000")
        instance.color = get_color_from_hex("#FFFFFF")
        instance.disabled = True

        for button in self.botao_classes:
            if button.jogador_index == jogador_index and button.text != escolha:
                button.disabled = True

            if button.jogador_index != jogador_index and button.text == escolha:
                button.disabled = True

        if all(button.disabled for button in self.botao_classes):
            print("Jogadores entraram na caverna!")
            game_state.print_game_state()
            app.root.current = "desafios"

class DesafiosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=1, spacing=10)

        label = Label(text="Tela dos Desafios", font_size=20)
        self.layout.add_widget(label)

        self.botao_avancar = Button(text="Avançar para o desafio")
        self.botao_avancar.bind(on_press=self.avancar)
        self.layout.add_widget(self.botao_avancar)

        self.botao_sair = Button(text="Reiniciar a Caverna")
        self.botao_sair.bind(on_press=self.sair)
        self.layout.add_widget(self.botao_sair)

        self.add_widget(self.layout)

        game_state.display_situacao()
    
    def avancar(self, instance):
        print("Avançando para o desafio...")
        app.root.current = "jogar_dados"

    def sair(self, instance):
        print("Reiniciando a caverna...")
        self.manager.current = "menu"

class JogarDadosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numero_aleatorio = None

        self.layout = BoxLayout(orientation='vertical', spacing=10)

        self.botao_dados = Button(text="Dados", valign='middle', halign='center', size_hint=(1, 1), width=100, height=100, font_size=90, disabled=True)
        self.botao_dados.bind(size=self.botao_dados.setter('text_size'))
        self.layout.add_widget(self.botao_dados)

        self.botao_jogar_dados = Button(text="Jogar Dados", size_hint=(1, None), width=150, height=50)
        self.botao_jogar_dados.bind(on_press=self.jogar_dados)
        self.layout.add_widget(self.botao_jogar_dados)

        self.botao_avancar = Button(text="Avançar", size_hint=(1, None), width=150, height=50, disabled=True)
        self.botao_avancar.bind(on_press=lambda instance: self.avancar(self.numero_aleatorio))
        self.layout.add_widget(self.botao_avancar)

        self.add_widget(self.layout)

    def jogar_dados(self, instance):
        self.botao_jogar_dados.disabled = True

        self.numero_aleatorio = random.randint(1, 6)  
        self.botao_dados.text = "0"

        print("Jogando dados:", self.numero_aleatorio)

        def atualizar_label(dt):
            if int(self.botao_dados.text) < self.numero_aleatorio:
                self.botao_dados.text = str(int(self.botao_dados.text) + 1)
            else:
                Clock.unschedule(atualizar_label)
                self.botao_avancar.disabled = False  

        Clock.schedule_interval(atualizar_label, 0.5)
    
    def avancar(self, numero_aleatorio):
        if numero_aleatorio is None:
            print("Erro: o número aleatório não foi gerado ainda.")
            return
        
        if numero_aleatorio % 2 == 0:
            app.root.current = "explorar"
            print("Avançando para a tela de exploração...")

        else:
            game_state.criar_inimigo()
            app.root.current = "confronto" 
            print("Avançando para a tela de confronto...")

        self.botao_avancar.disabled = True
        self.botao_jogar_dados.disabled = False

class ExplorarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rd = random.randint(1, 2)
        print(f"Os dados foram {self.rd}")
        self.game_state = game_state
        self.layout = BoxLayout(orientation='vertical', spacing=10)
        self.num_exploracoes = 1
        
        label = Label(text="Você avança pela caverna escura, ouvindo o eco dos seus passos nas paredes de pedra.")
        self.layout.add_widget(label)

        self.info_label = Label(text="Escolha a ação do grupo!", font_size=20)
        self.layout.add_widget(self.info_label)

        self.situacao_label = Label(text='', font_size=16)
        self.layout.add_widget(self.situacao_label)
        game_state.display_situacao()
        self.situacao_label.text = game_state.classes_label.text

        avancar_button = Button(text="Avançar")
        avancar_button.bind(on_release=self.avancar)
        self.layout.add_widget(avancar_button)

        esquerda_button = Button(text="Virar à Esquerda")
        esquerda_button.bind(on_release=self.virar_esquerda)
        self.layout.add_widget(esquerda_button)

        direita_button = Button(text="Virar à Direita")
        direita_button.bind(on_release=self.virar_direita)
        self.layout.add_widget(direita_button)

        descansar_button = Button(text="Descansar")
        descansar_button.bind(on_release=self.descansar)
        self.layout.add_widget(descansar_button)

        sair_button = Button(text="Reiniciar a Caverna")
        sair_button.bind(on_release=self.exit_caverna)
        self.layout.add_widget(sair_button)

        self.add_widget(self.layout)
        

    def update_info_label(self, text):
        self.info_label.text = text

    def avancar(self, instance):
        self.num_exploracoes += 1
        self.aumento = 10 + self.num_exploracoes
        for jogador in game_state.jogadores:
            if jogador.dano < 0:
                jogador.dano -= self.aumento
            else:
                jogador.dano += self.aumento
        resultados = "Aventureiros corajosos avançaram de peito aberto.\nTodos ganham {} de dano.\n".format(self.aumento)
        som = 1
        app.root.current = "resultadoe"
        app.root.get_screen("resultadoe").mostrar_resultado(resultados)
        app.root.get_screen("resultadoe").som(resultados)

    def virar_esquerda(self, instance):
        self.num_exploracoes += 1
        self.aumento = 20 + self.num_exploracoes
        self.reduz = 50 + self.num_exploracoes
        resultados = ""
        som = None
        if self.rd == 2:
            resultados = "Viraram à esquerda derraparam em uma passagem estreita.\nTodos perdem {} de vida.\n".format(self.reduz)
            som = 2
            for jogador in game_state.jogadores:
                jogador.vida -= self.reduz
                
                if jogador.vida <=0:
                    fim = "O {} caiu em um precipício.\n".format(jogador.classe)
                    app.root.current = "final"
                    app.root.get_screen("final").mostrar_fim(fim)

        else:
            resultados = "Viraram à esquerda e encontraram uma sala misteriosa.\nTodos ganham {} de dano.\n".format(self.aumento)
            som = 1
            for jogador in game_state.jogadores:
                if jogador.dano < 0:
                    jogador.dano -= self.aumento
                else:
                    jogador.dano += self.aumento
            
        app.root.current = "resultadoe"
        app.root.get_screen("resultadoe").mostrar_resultado(resultados)
        app.root.get_screen("resultadoe").som(resultados)

    def virar_direita(self, instance):
        self.num_exploracoes += 1
        self.aumento = 20 + self.num_exploracoes
        self.reduz = 50 + self.num_exploracoes
        resultados = ""
        som = None
        if self.rd % 2 != 0:
            resultados = "Viraram à direita derraparam em uma passagem estreita.\nTodos perdem {} de vida.\n".format(self.reduz)
            som = 2
            for jogador in game_state.jogadores:
                jogador.vida -= self.reduz
        else:
            resultados = "Viraram à direita e encontraram uma sala misteriosa.\nTodos ganham {} de dano.\n".format(self.aumento)
            som = 1
            for jogador in game_state.jogadores:
                if jogador.dano < 0:
                    jogador.dano -= self.aumento
                else:
                    jogador.dano += self.aumento
            
        app.root.current = "resultadoe"
        app.root.get_screen("resultadoe").mostrar_resultado(resultados)
        app.root.get_screen("resultadoe").som(resultados)

    def descansar(self, instance):
        self.num_exploracoes += 1
        self.aumento = 30 + self.num_exploracoes
        resultados = "Precisaram descansar para recuperar um pouco de suas condições.\nTodos ganham {} de vida.\n".format(self.aumento)
        som = 1
        for jogador in game_state.jogadores:
                jogador.vida += self.aumento
        app.root.current = "resultadoe"
        app.root.get_screen("resultadoe").mostrar_resultado(resultados)
        app.root.get_screen("resultadoe").som(resultados)

    def exit_caverna(self, instance):
        self.manager.current = "menu"

class ConfrontoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Número de jogadores:", len(game_state.jogadores))

        self.layout = GridLayout(cols=1, spacing=10)
        self.classes_label = Label()
        self.layout.add_widget(self.classes_label)
        
        atacar_button = Button(text="Atacar")
        atacar_button.bind(on_release=self.on_attack)
        self.layout.add_widget(atacar_button)

        defender_button = Button(text="Defender")
        defender_button.bind(on_release=self.on_defend)
        self.layout.add_widget(defender_button)

        curar_button = Button(text="Curar")
        curar_button.bind(on_release=self.on_heal)
        self.layout.add_widget(curar_button)

        sair_button = Button(text="Reiniciar a caverna")
        sair_button.bind(on_release=self.sair)
        self.layout.add_widget(sair_button)

        self.add_widget(self.layout)

        self.current_player_index = 0
        self.display_jogador()

        sound = SoundLoader.load('data/inimigo.mp3')
        if sound:
            sound.play()
        else:
            print("Erro: Não foi possível carregar o arquivo de áudio")

    def display_jogador(self):
        
        print("Index do jogador atual:", self.current_player_index)
        if self.current_player_index < len(game_state.jogadores):
            jogador = game_state.jogadores[self.current_player_index] 
            text = f"O inimigo está na sua frente!\nEle tem {game_state.inimigo.vida} de vida e {game_state.inimigo.dano} de dano.\n\n{jogador.classe} tem {jogador.vida} de vida e {jogador.dano} de dano"
            self.classes_label.text = text
            self.classes_label.halign = 'center'
        else:
            print("Todos os jogadores realizaram suas ações. Vez do inimigo...")
            self.enemy_attack()
    
    def on_pre_enter(self, *args):
        print("Acessando dados atualizados do game_state...")
        self.display_jogador()
    
    def on_attack(self, instance):
        print("Você escolheu atacar!")
        jogador = game_state.jogadores[self.current_player_index] 
        print(f"{jogador.classe} atacou o inimigo com {game_state.inimigo.vida} e causou {jogador.dano} de dano.")
        game_state.inimigo.vida -= jogador.dano

        if game_state.inimigo.vida <= 0:
            print("Você derrotou o inimigo!\n")
            self.aumento = 50*game_state.inimigo.derrotado + 2*game_state.inimigo.derrotado
            self.aumento1 = 20 + game_state.inimigo.derrotado *2
            game_state.inimigo.derrotado += 1
            resultados = f"O {jogador.classe} derrotou o inimigo!\n\nTodos ganham {self.aumento} de vida e {self.aumento1} de dano."
            for jogador in game_state.jogadores:
                jogador.vida += self.aumento
                if jogador.dano>0:
                    jogador.dano += self.aumento1
                else:
                    jogador.dano -= self.aumento1
            self.current_player_index = 0
            app.root.current = "resultadoa"
            app.root.get_screen("resultadoa").mostrar_resultado(resultados)
            return

        self.current_player_index += 1 
        if self.current_player_index >= len(game_state.jogadores):
            print("Todos os jogadores realizaram suas ações. Vez do inimigo...")
            self.enemy_attack()
        
        sound = SoundLoader.load('data/ataque.mp3')
        if sound:
            sound.play()
        else:
            print("Erro: Não foi possível carregar o arquivo de áudio")

        self.display_jogador()
    
    def on_defend(self, instance):
        print("Você escolheu defender!")
        jogador = game_state.jogadores[self.current_player_index] 
        cura = int(jogador.dano * 2/3)  
        print(f"{jogador.classe} fortaleceu sua defesa e aumentou {cura} de sua vida.")
        jogador.vida += cura
        self.current_player_index += 1
        self.display_jogador()
    
    def on_heal(self, instance):
        print("Você escolheu curar!")
        healer = game_state.jogadores[self.current_player_index]
        menorvida = 999999
        curado = None
    
        for jogador in game_state.jogadores:
            if jogador.vida < menorvida:
                menorvida = jogador.vida
                curado = jogador
    
        if curado is not None:
            curado.vida -= healer.dano
            print(f"{curado.classe} foi curado e recuperou {-healer.dano} de vida.")
        
            if curado.vida <= 0:
                print("Você derrotou o aliado!\n")
                self.manager.current = "menu"

        self.current_player_index += 1
        self.display_jogador()

    def sair(self, instance):
        print("Reiniciando a caverna...")
        self.manager.current = "menu" 

    def next_player(self):
        if len(game_state.jogadores) == 0:
            print("Todos os jogadores realizaram suas ações. Vez do inimigo...")
            self.enemy_attack()
        else:
            proximo_jogador = game_state.jogadores.pop(0)
            print(f"Vez do próximo jogador: {proximo_jogador.classe}")      

    def enemy_attack(self):
        if game_state.inimigo is None:
            print("Erro: O inimigo não está definido.")
            return

        self.aleatorio = random.randint(1, 2)
        print(f"Os dados foram {self.aleatorio}")
        resultados = ""

        if hasattr(game_state.inimigo, 'dano'):
            self.dano = game_state.inimigo.dano
            if self.aleatorio == 1:
                for jogador in game_state.jogadores:
                    jogador.vida -= (self.dano / game_state.num_jogadores)
                    if jogador.vida <= 0:
                        print("O inimigo te derrotou!\n")
                        fim = "O inimigo utilizou ataque de {} e derrotou {}.\n".format(self.dano, jogador.classe)
                        app.root.current = "final"
                        app.root.get_screen("final").mostrar_fim(fim) 
                        return
                resultados = "O inimigo utilizou ataque em área.\nTodos perdem {} de vida.\n".format(self.dano / game_state.num_jogadores)
                    
            else:
                maiorvida = 0
                atacado = None
                for jogador in game_state.jogadores:
                    if jogador.vida > maiorvida:
                        maiorvida = jogador.vida
                        atacado = jogador
        
                if atacado is not None:
                    atacado.vida -= self.dano
                    resultados = "{} foi atacado pelo inimigo e perdeu {} de vida.".format(atacado.classe, self.dano)

                if atacado is not None and atacado.vida <= 0:
                    print("O inimigo te derrotou!\n")
                    self.manager.current = "menu"
                    fim = "O inimigo utilizou ataque de {} e derrotou {}.\n".format(self.dano, atacado.classe)
                    app.root.current = "final"
                    app.root.get_screen("final").mostrar_fim(fim) 
                    return
                    
        self.current_player_index = 0
        app.root.current = "resultadoa"
        app.root.get_screen("resultadoa").mostrar_resultado(resultados)

class ResultadoAScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.label_resultado = Label(text="Vez do inimigo atacar!")
        self.layout = BoxLayout(orientation='vertical', spacing=10)

        self.label_resultado.text = "Resultado do confronto"
        self.layout.add_widget(self.label_resultado)
        self.button_confronto = Button(text="Atacar o inimigo", halign = 'center', font_size=20)
        self.button_confronto.bind(on_press=self.voltar_para_confronto)
        self.layout.add_widget(self.button_confronto)
        self.button_voltar = Button(text="Esse foi!\nBora de next...", halign = 'center', font_size=20)
        self.button_voltar.bind(on_press=self.voltar_para_desafios)
        self.layout.add_widget(self.button_voltar)
        self.add_widget(self.layout)

        sound = SoundLoader.load('data/inimigo.mp3')
        if sound:
            sound.play()
        else:
            print("Erro: Não foi possível carregar o arquivo de áudio")

    def voltar_para_confronto(self, instance):
        app.root.current = "confronto"
        self.current_player_index = 0

    def voltar_para_desafios(self, instance):
        self.button_confronto.disabled = False
        app.root.current = "desafios"

    def mostrar_resultado(self, resultados):
        atributos = game_state.jogadores
        self.label_resultado.text = resultados

        if game_state.inimigo.vida <= 0:   
            self.button_confronto.disabled = True

        atributos_text = "\n".join([f"{jogador.nome}: Classe {jogador.classe} tem {jogador.vida} de Vida e {jogador.dano} de Dano" for jogador in atributos])
        self.label_resultado.text += f"\nSituação dos Jogadores:\n{atributos_text}"
        self.label_resultado.halign = 'center'

class ResultadoEScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.label_resultado = Label(text="Agora que decidiram:")
        self.layout = BoxLayout(orientation='vertical', spacing=10)

        self.label_resultado.text = "Resultado da exploração"  # Definido temporariamente
        self.layout.add_widget(self.label_resultado)
        self.button_voltar = Button(text="Bora para novos desafios", font_size=20)
        self.button_voltar.bind(on_press=self.voltar_para_desafios)
        self.layout.add_widget(self.button_voltar)
        self.add_widget(self.layout)

    def som(self, som):
        self.sound = som
        if som ==1:
            sound = SoundLoader.load('data/buff.mp3')
            if sound:
                sound.play()
            else:
                print("Erro: Não foi possível carregar o arquivo de áudio")
        
        if som ==2:
            sound = SoundLoader.load('data/queda.mp3')
            if sound:
                sound.play()
            else:
                print("Erro: Não foi possível carregar o arquivo de áudio")

    def mostrar_resultado(self, resultados):
        atributos = game_state.jogadores
        self.label_resultado.text = resultados
        
        atributos_text = "\n".join([f"{jogador.nome}: Classe {jogador.classe} tem {jogador.vida} de Vida e {jogador.dano} de Dano" for jogador in atributos])
        self.label_resultado.text += f"\nSituação dos Jogadores:\n{atributos_text}"      
        self.label_resultado.halign = 'center'

    def voltar_para_desafios(self, instance):
        app.root.current = "desafios"

class FinalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.label = Label(text="Acabou a aventura:")
        self.layout = BoxLayout(orientation='vertical', spacing=10)

        self.label_fim = Label(text="", font_size=20)
        self.layout.add_widget(self.label_fim)

        self.button_voltar = Button(text="Começar uma nova aventura?", font_size=20)
        self.button_voltar.bind(on_press=self.voltar_para_menu)
        self.layout.add_widget(self.button_voltar)

        self.add_widget(self.layout)
        self.perdeu()

    def perdeu(self):
        sound = SoundLoader.load('data/perdeu.mp3')
        if sound:
            sound.play()
        else:
            print("Erro: Não foi possível carregar o arquivo de áudio")

    def voltar_para_menu(self, instance):
        app.root.current = "menu"

    def mostrar_fim(self, fim):
        self.label_fim.text = fim

class RPGTxt(App):
    def build(self):
        self.sm = ScreenManager()
        self.main_menu = MainMenu(name="menu")
        self.num_jogadores_screen = NumJogadoresScreen(name="num_jogadores")
        self.classe_selection_screen = ClasseSelectionScreen(num_jogadores=game_state.num_jogadores, name="classe_selection")  # Passando o argumento num_jogadores
        self.desafios_screen = DesafiosScreen(name="desafios")
        self.jogar_dados_screen = JogarDadosScreen(name="jogar_dados")
        self.explorar_screen = ExplorarScreen(name="explorar")
        self.confronto_screen = ConfrontoScreen(name="confronto")
        self.resultadoa_screen = ResultadoAScreen(name="resultadoa")
        self.resultadoe_screen = ResultadoEScreen(name="resultadoe")
        self.final_screen = FinalScreen(name="final")
        self.sm.add_widget(self.main_menu)
        self.sm.add_widget(self.num_jogadores_screen)
        self.sm.add_widget(self.classe_selection_screen)
        self.sm.add_widget(self.desafios_screen)
        self.sm.add_widget(self.jogar_dados_screen)
        self.sm.add_widget(self.explorar_screen)
        self.sm.add_widget(self.confronto_screen)
        self.sm.add_widget(self.resultadoa_screen)
        self.sm.add_widget(self.resultadoe_screen)
        self.sm.add_widget(self.final_screen)
        
        sound = SoundLoader.load('data/caverna.mp3')
        if sound:
            sound.play()
        else:
            print("Erro: Não foi possível carregar o arquivo de áudio")
        return self.sm
    
if __name__ == '__main__':
    app = RPGTxt()
    app.run()