# Survivor Coursework Project

![Game Cover](Assets/UI/images/cover2.png)

## 🎮 About The Game

2D survivor style game, inspired by vampire survivors. Procedurally generated map, different guns, enemies and more.

## 🚀 Features

- Engaging 2D top-down gameplay
- Multiple weapons with unique characteristics
- Perlin noise-generated environments
- Advanced particle systems for visual effects
- Customizable game settings

## 🖼 Screenshots

![Gameplay Screenshot](Assets/UI/images/game_screenshot.png)

## 📦 Dependencies

To run this game, you'll need the following Python packages listed in the requirements.txt

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

### Installation

1. Clone the repository
   git clone https://github.com/yourusername/survivor-coursework.git
2. Navigate to the project directory
   cd survivor-coursework-project
3. Install required packages
   pip install -r requirements.txt

### Running the Game

Simply run the provided "run.exe" file to start the game.

## 🎛 Controls

- WASD: Move the player
- Mouse: Aim
- Left Click: Shoot
- Shift: Sprint
- Jump: Space
- ESC: Pause game

### Packaging the Game

To create an executable, use pyinstaller:

```bash
pyinstaller --clean --icon=C:\Users\digot\PycharmProjects\Survivor-Coursework-Project\Assets\UI\images\cover.png Run.py --onedir --windowed --noconsole --add-data "Code:Code"
```

## 👨‍💻 Authors

 -[Digotill](https://github.com/digotill)

## 📄 License

This project is licensed under the [MIT license] - see the [LICENSE](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Special thanks to [DaFluffyPotato](https://github.com/DaFluffyPotato) for some of the code used in this project
  - Grass system implementation
- Inspiration drawn from various top-down survival games
- Thanks to the Pygame and OpenGL communities for their excellent libraries and documentation
