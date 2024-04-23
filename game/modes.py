import pickle

from flappy_bird.maps import MapHandler
from flappy_bird.objects import Character
from .environment import Environment
import pygame
from game import WINDOW_WIDTH, TICK_RATE
from flappy_bird import SPEED_CHANGE_EVERY
import neat


FLOOR = 730
gen = 0
class TestAI(Environment):
    # Modified the draw to be able to draw multiple birds
    def draw(self,win, birds, score, gen, pipe_ind):
        win.blit(self.map.bg, (0, 0))

        for pipe in self.map.pipes:
            pipe.draw(win)
        
        text = self.font.render("Score: " + str(score), 1, (255,255,255)) 
        win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

        self.map.floor.draw(win)
        for bird in birds:
            # draw bird
            bird.draw(win)
        # generations
        score_label = self.font.render("Gens: " + str(gen-1),1,(255,255,255))
        win.blit(score_label, (10, 10))

        # alive
        score_label = self.font.render("Alive: " + str(len(birds)),1,(255,255,255))
        win.blit(score_label, (10, 50))

        # speed
        score_label = self.font.render("Speed: " + str(self.map.PIPE_VEL),1,(255,255,255))
        win.blit(score_label, (10, 100))
        pygame.display.update()

    # Run was modified to not use the default loop. Neat requires to run the loop/eval_genomes on its own
    def run(self):
        """
        runs the NEAT algorithm to train a neural network to play flappy bird.
        :param config_file: location of config file
        :return: None
        """
        
        config_file = "./config-feedforward.txt"
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_file)

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        #p.add_reporter(neat.Checkpointer(5))

        def eval_genomes(genomes, config):
            """
            runs the simulation of the current population of
            birds and sets their fitness based on the distance they
            reach in the game.
            """
            global gen
            win = self.win
            gen += 1

            # start by creating lists holding the genome itself, the
            # neural network associated with the genome and the
            # bird object that uses that network to play
            nets = []
            birds = []
            ge = []
            for genome_id, genome in genomes:
                genome.fitness = 0  # start with fitness level of 0
                net = neat.nn.FeedForwardNetwork.create(genome, config)
                nets.append(net)
                birds.append(self.char.__class__(230,350))
                ge.append(genome)
            score = 0

            clock = pygame.time.Clock()

            run = True
            while run and len(birds) > 0:
                clock.tick(TICK_RATE)                
                pipe_ind = 0
                if len(birds) > 0:
                    if len(self.map.pipes) > 1 and birds[0].x > self.map.pipes[0].x + self.map.pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                        pipe_ind = 1 # pipe on the screen for neural network input
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        quit()
                        break
                for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
                    ge[x].fitness += 0.1
                    bird.move()

                    # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
                    output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - self.map.pipes[pipe_ind].height), abs(bird.y - self.map.pipes[pipe_ind].bottom)))
                    

                    if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                        bird.jump()
                rem = []
                add_pipe = False
                self.map.floor.move() # Handles the movement of the floor
                for pipe in self.map.pipes:
                    # check for collision
                    for bird in birds:
                        if pipe.collide(bird):
                            ge[birds.index(bird)].fitness -= 1
                            nets.pop(birds.index(bird))
                            ge.pop(birds.index(bird))
                            birds.pop(birds.index(bird))

                    if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                        rem.append(pipe)

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True
                    
                    pipe.move()

                if add_pipe:
                    score += 1
                    # can add this line to give more reward for passing through a pipe (not required)
                    for genome in ge:
                        genome.fitness += 5
                    self.map.pipes.append(self.map.create_pipe())
                    add_pipe = False

                # Remove pipes that are off screen
                    if score % SPEED_CHANGE_EVERY == 0:
                        self.map.set_speed_map(self.map.PIPE_VEL + 1) # Increase the speed of the map every 5 points
                        
                for r in rem:
                    self.map.pipes.remove(r)

                for bird in birds:
                    if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                        nets.pop(birds.index(bird))
                        ge.pop(birds.index(bird))
                        birds.pop(birds.index(bird))

                # break if score gets large enough
                """ if score > 200:
                    pickle.dump(nets[0],open("best.pickle", "wb"))
                    break """
                
                self.draw(win,birds,score,gen,pipe_ind)

            #At this point, all birds are extinct, but new generations will spawn
            # Remove all pipes when starting a new generation
            self.map.pipes = [self.map.create_pipe()]
            self.map.set_to_default_speed()
            # Change map on reset
            new_map = self.map.new_map()
            self.map.change_map(new_map)
        # Full evolution is complete
        # Run for up to 50 generations.
        winner = p.run(eval_genomes, 50)

        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))
        """ with open("winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close() """

class Solo(Environment):
    def collide_handler(self):
        self.is_finished = True
        self.game_over_prompt()
        
    def controls(self, event):
        """Handles the controls for the game"""
        if event.type == pygame.KEYDOWN:
            if self.is_finished:
                # user selects which option to choose after game over
                if event.key == pygame.K_LEFT:
                    # user selects restart
                    self.selected_option = 0
                    # redraw grame over prompt
                    self.game_over_prompt()
                if event.key == pygame.K_RIGHT:
                    # user selects exit
                    self.selected_option = 1
                    # redraw grame over prompt
                    self.game_over_prompt()
                # user confirms decision
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # restart                 
                    if self.selected_option == 0:
                        return self.restart()
                    # exit to menu
                    else:
                        return self.exit_mode()


            if not self.is_finished:     
                if event.key == pygame.K_SPACE:
                    return self.char.jump()
                
                # if event.key == pygame.K_ESCAPE:
                #     return self.game_over_prompt()
                
    def game_over_prompt(self):
        """This will prompt the game over message"""
        # draw game over title
        gameover_font = pygame.font.Font("./assets/fonts/Minercraftory.ttf", 45)
        gameover_text = gameover_font.render("GAME OVER", True, (255, 255, 255))
        gameover_text_rect = gameover_text.get_rect(center=(WINDOW_WIDTH/2, 150))
        self.win.blit(gameover_text, gameover_text_rect)
        # draw score
        score_font = pygame.font.Font("./assets/fonts/Minercraftory.ttf", 25)
        score_text = score_font.render("Score " + str(self.score), 1, (255,255,255)) 
        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, 220))
        self.win.blit(score_text, score_text_rect)
        # draws rectangle
        # rectangle border
        pygame.draw.rect(self.win, (214,168,74), (45, 245, 410, 210), border_radius=10)
        # rectangle bezel
        pygame.draw.rect(self.win, (255,234,163), (50, 250, 400, 200), border_radius=10)
        # rectangle bezel inside border
        pygame.draw.rect(self.win, (214,168,74), (61, 261, 378, 178), border_radius=10)
        # rectangle inside
        pygame.draw.rect(self.win, (255,234,163), (65, 265, 370, 170), border_radius=10)
        # draw play button
        play = pygame.image.load('./assets/general/play.svg')
        # scale button if it's selected
        if(self.selected_option == 0):
            play = pygame.transform.scale(
                play, (60,65)
            )
            self.win.blit(play, (125, 312))
        else:
            play = pygame.transform.scale(
                play, (50,55)
            )
            self.win.blit(play, (130, 317))
        # draw menu button
        menu = pygame.image.load('./assets/general/menu.svg')
        # scale button if it's selected
        if(self.selected_option == 1):
            menu = pygame.transform.scale(
                menu, (60,65)
            )
            self.win.blit(menu, (295, 312))
        else:
            menu = pygame.transform.scale(
                menu, (50,55)
            )
            self.win.blit(menu, (300, 317))
        pygame.display.update()
    
class AIvsPlayer(Environment):
    """The environment class for the game"""
    def __init__(self, win, maps: MapHandler, char: Character):
        super().__init__(win, maps, char)
        self.ai = None
        self.ai_character = Character.characters_available()[0](100, 670)
        self.ai_dead = False
        self.ai_score = 0
    def collide_handler(self):
        self.is_finished = True
        self.game_over_prompt()
    
    def _collided(self):
        """This handles the collision of the character with the floor and pipes"""
        if self.map.floor.collide(self.ai_character):
            self.ai_dead = True               

        if self.map.floor.collide(self.char):
            return self.collide_handler()
            pass
        
        for pipe in self.map.pipes:
            if pipe.collide(self.ai_character):
                self.ai_dead = True
            if pipe.collide(self.char):
                return self.collide_handler()
                pass

    def controls(self, event):
        """Handles the controls for the game"""
        if event.type == pygame.KEYDOWN:
            if self.is_finished:
                # user selects which option to choose after game over
                if event.key == pygame.K_LEFT:
                    # user selects restart
                    self.selected_option = 0
                    # redraw grame over prompt
                    self.game_over_prompt()
                if event.key == pygame.K_RIGHT:
                    # user selects exit
                    self.selected_option = 1
                    # redraw grame over prompt
                    self.game_over_prompt()
                # user confirms decision
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # restart                 
                    if self.selected_option == 0:
                        return self.restart()
                    # exit to menu
                    else:
                        return self.exit_mode()


            if not self.is_finished:     
                if event.key == pygame.K_SPACE:
                    return self.char.jump()
                
                # if event.key == pygame.K_ESCAPE:
                #     return self.game_over_prompt()
                
    def game_over_prompt(self):
        """This will prompt the game over message"""
        # draw game over title
        gameover_font = pygame.font.Font("./assets/fonts/Minercraftory.ttf", 45)
        gameover_text = gameover_font.render("GAME OVER", True, (255, 255, 255))
        gameover_text_rect = gameover_text.get_rect(center=(WINDOW_WIDTH/2, 150))
        self.win.blit(gameover_text, gameover_text_rect)
        # draw score
        score_font = pygame.font.Font("./assets/fonts/Minercraftory.ttf", 25)
        score_text = score_font.render("Score " + str(self.score), 1, (255,255,255)) 
        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, 220))
        self.win.blit(score_text, score_text_rect)
        # draws rectangle
        # rectangle border
        pygame.draw.rect(self.win, (214,168,74), (45, 245, 410, 210), border_radius=10)
        # rectangle bezel
        pygame.draw.rect(self.win, (255,234,163), (50, 250, 400, 200), border_radius=10)
        # rectangle bezel inside border
        pygame.draw.rect(self.win, (214,168,74), (61, 261, 378, 178), border_radius=10)
        # rectangle inside
        pygame.draw.rect(self.win, (255,234,163), (65, 265, 370, 170), border_radius=10)
        # draw play button
        play = pygame.image.load('./assets/general/play.svg')
        # scale button if it's selected
        if(self.selected_option == 0):
            play = pygame.transform.scale(
                play, (60,65)
            )
            self.win.blit(play, (125, 312))
        else:
            play = pygame.transform.scale(
                play, (50,55)
            )
            self.win.blit(play, (130, 317))
        # draw menu button
        menu = pygame.image.load('./assets/general/menu.svg')
        # scale button if it's selected
        if(self.selected_option == 1):
            menu = pygame.transform.scale(
                menu, (60,65)
            )
            self.win.blit(menu, (295, 312))
        else:
            menu = pygame.transform.scale(
                menu, (50,55)
            )
            self.win.blit(menu, (300, 317))
        pygame.display.update()

    def load_AI(self):
        config_path = "./config-feedforward.txt"
        # Load requried NEAT config
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

        # Unpickle saved winner
        with open("./winner.pkl", "rb") as f:
            winner = pickle.load(f)

        # Convert loaded genome into required data structure
        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
        self.ai = winner_net

    def loop(self):
        """Runs the game loop"""
        print("game loop start")
        self.load_AI()
        while self.is_running:
            #print(self.is_running)
            self.clock.tick(TICK_RATE)
            
            self._controls_loop() # Handles the controls loop for the game

            self._collided() # Handles the collides of the character with the floor and pipes
            pipe_ind = 0
            if not self.is_finished: # This will stop the game loop if the game is finished
                if len(self.map.pipes) > 1 and self.ai_character.x > self.map.pipes[0].x + self.map.pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                    pipe_ind = 1 # pipe on the screen for neural network input

                # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
                output = self.ai.activate((self.ai_character.y, abs(self.ai_character.y - self.map.pipes[pipe_ind].height), abs(self.ai_character.y - self.map.pipes[pipe_ind].bottom)))
                

                if output[0] > 0.5 and not self.ai_dead:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                    self.ai_character.jump()

                rem = []
                add_pipe = False 
                
                for pipe in self.map.pipes:
                    # If the pipe is off the screen, remove it
                    if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                        rem.append(pipe) 
                    # If the pipe is not passed and the character has passed it, add a new pipe
                    if not pipe.passed and pipe.x < self.char.x:
                        pipe.passed = True
                        self.score += 1
                        add_pipe = True

                    if not pipe.ai_passed and pipe.x < self.ai_character.x:
                        pipe.ai_passed = True
                        self.ai_score += 1

                    pipe.move()
                    
                    
                if add_pipe:
                    # If the character has passed the pipe, add a new pipe and increment the score
                    self.map.pipes.append(self.map.create_pipe())
                    add_pipe = False
                    
                    if self.score % SPEED_CHANGE_EVERY == 0:
                        self.map.set_speed_map(self.map.PIPE_VEL + 1) # Increase the speed of the map every 5 points
                # Remove the pipes that are off the screen
                for r in rem:
                    self.map.pipes.remove(r)

                self.char.move() # Handles the movement of the character
                self.ai_character.move()
                self.map.floor.move() # Handles the movement of the floor

                self.draw() # Draws the game
        print("game is no longer running")
    
    def draw(self):
        self.win.blit(self.map.bg, (0, 0))

        for pipe in self.map.pipes:
            pipe.draw(self.win)
        
        text = self.font.render("Score: " + str(self.score), 1, (255,255,255)) 
        self.win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))
        
        text = self.font.render("AI Score: " + str(self.ai_score), 1, (255,255,255)) 
        self.win.blit(text, (5, 10))

        self.map.floor.draw(self.win)
        self.char.draw(self.win)
        self.ai_character.draw(self.win)
        pygame.display.set_caption("Flappy Bird")
        pygame.display.update()
    
    def restart(self):
        """Restarts the game if the game is finished"""
        # Resart the game
        if self.is_finished:
            new_map = self.map.new_map()
            self.map.change_map(new_map)
            self.char.y = 350
            self.ai_character.y = 350
            self.map.pipes = [self.map.create_pipe()]
            self.score = 0
            self.ai_score = 0
            self.run()
            