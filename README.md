# AlpaRun
#### Video Demo: https://youtu.be/0Uq5jGI7cX4

#### Description:

AlpaRun is a simple running game featuring a white alpaca running on a track to reach the doughnut in the sky.
The objective of the game is to control the alpaca's movements and guide it to stay on the track (using left and right control keys) while chasing the unreachable doughnut.

Developing this game has been an incredible experience for me, especially considering it's my first foray into app creation. I dedicated over 40 hours to the development process, and I must say, it was quite the learning curve. Along the way, I encountered my fair share of debugging challenges and moments of frustration. However, I persevered and found joy in the process.

Initially, I started by following a tutorial to create a basic clone, but as time went on, I couldn't resist adding my own personal touches. I wanted to create a game that was accessible to everyone, with simple mechanics that anyone could enjoy. AlpaRun gradually transformed into a unique and captivating experience.

#### Code details:

This project used Kivy 2.2.1 and is based on Jonathan Roux's tutorials.

main.py: This file contains essential code for game initialization, such as setting up the game window and loading assets. It also includes update functions that handle the game's logic, such as tracking the alpaca's movement and detecting collisions.
menu.py: For start and game over menus
game_speed.py: This file handles the gradual increase in game speed over time, adding excitement and challenge as the game progresses.
perspective.py: To switch the perspective to 2D
user_control: This module enables user control through keyboard input, allowing players to interact with the game.
audio/ fonts/ images/ : These folders contain the assets used in the game. Some assets are original, while others have been modified to suit the game's requirements.
kv files: Still far from master the basic use of the framework but I used alparun.kv for the main user interface.

### Assets:

I apologize for not being able to keep track of the origin of these files. The original author retains the rights, and if there are any issues, please contact me to request removal, or I will be happy to change the assets accordingly.

audio/
bell.wav: A bicycle bell used to signal the increase in speed.
gallop.wav: An actual horse sound.
game_start.wav: An alpaca sound played at the start of the game.
game_over.wav: An alpaca sound used to indicate game over.
rainbow_speed.wav: I wanted the music tempo to increase during gameplay, but I couldn't find a dynamic way to achieve it in the game. So, I decided to solve this by using a fixed increase in the wav file. Hopefully, no player will survive in the game long enough to break this.
rainbow.wav: A normal rhythm used in the start menu.

fonts/
Cheerful Dynamite and Seventies Sunrise

images/
alpa_run.gif: A loop of the alpaca running animation.
doughnut.gif: A flying chocolate doughnut in the sky.
drooling.gif: A drooling thought bubble that activates during speed increase to add interaction with the alpaca.

#### Design choices:

Graphics: The game features 2D sprites that aim to create a sense of simplicity, cuteness, and friendliness. Additionally, I wanted to capture the nostalgic vibe of the old SNES game era, which adds a touch of retro charm to the visuals. Enhacning the immersion factor with perspective tricks, allowing the game to create an illusion of depth and a more immersive experience for the players.

Controls and Gameplay Mechanics: I originally intended it to be a mobile game with only touch controls, allowing players to move left and right. This design choice was made to maintain the simplicity of the game and make it accessible to a wide range of players. By having minimal controls, the game allows players to focus on a single, straightforward task. The intention was to create a no-brainer game that people can play to have fun and relax, without the need for complex inputs or strategies.

Game Duration:  I want each round to be relatively short, lasting around 1 minute. I believe this duration aligns well with people's attention spans, allowing them to engage in quick gameplay sessions when they are bored or have a little time to spare.

Difficulty and Progression: The game incorporates a gradual increase in speed over time, which adds to the challenge and fun factor. The game starts with an easy difficulty level and progressively becomes more challenging as the speed increases. This gradual progression allows players to familiarize themselves with the gameplay mechanics and gradually improve their skills as they advance through the game.

#### Final thoughts:

Right now, my code is a bit messy, but my main goal is to make everything work smoothly. However, I know there's room for improvement in designing the game and planning for the future. If I focus on better game design and think ahead, it will make things easier as the game develops further.

To improve the game's design, I plan to organize and optimize my code later, making it easier to read and maintain. I'll also consider potential features like new levels or special events. By better planning, I can save time and effort when adding new content.

I'll seek learning opportunities, such as taking courses, to enhance my software development skills. This will help me create better games in the future.

AlpaRun has motivated me to grow as a developer. By focusing on game design and planning for the future, I can continue to learn and create exciting projects.

Lastly, I am still unsure about how to package this game. I would love to be able to send it to my friends on desktop, mobile, or web platforms so they can try it out. If anyone is interested in porting or creating a package for this game, please guide me on how to proceed.