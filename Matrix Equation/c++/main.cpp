#include <iostream>
#include <random>
#include <SFML/Graphics.hpp>
#include <Eigen/Dense>

using namespace std;

using Eigen::Matrix2f;
using Eigen::Vector2f;

random_device rd;
mt19937 gen(rd());
uniform_int_distribution<int> dis(0, 5);

sf::Vector2f oldPos;
bool moving = false;


const int Max = 1e3;
float dt = 1/2;
const int Scale = 1024;
float zoom = 1;
int Coords[Scale][Scale] = {0};



void manageEvents(sf::RenderWindow &window) {
    for (auto event = sf::Event(); window.pollEvent(event);) {
        if (event.type == sf::Event::Closed) {
            window.close();
        } else if (event.type == sf::Event::KeyPressed) {
            if (event.key.code == sf::Keyboard::Escape) {
                window.close();
            } else if (event.key.code == sf::Keyboard::R) {
                // Reset the view on R
                window.clear();
                sf::View view(sf::FloatRect(0, 0, Scale, Scale));
                window.setView(view);
            }
        } else if (event.type == sf::Event::Resized) {
            auto view = window.getView();
            view.setSize(event.size.width, event.size.height);
            window.setView(view);
        } else if (event.type == sf::Event::MouseWheelScrolled) {
            if (event.mouseWheelScroll.delta <= -1)
                zoom = min(1.f, zoom + .1f);
            else if (event.mouseWheelScroll.delta >= 1)
                zoom = max(.02f, zoom - .1f);

            // Update our view
            window.clear();
            auto view = window.getView(); // Get the current view
            view.setSize(window.getDefaultView().getSize()); // Reset the size
            view.zoom(zoom); // Apply the zoom level (this transforms the view)
            window.setView(view);
            break;
        } else if (event.type == sf::Event::MouseButtonPressed) {
            // Mouse button is pressed, get the position and set moving as active
            if (event.mouseButton.button == 0) {
                moving = true;
                oldPos = window.mapPixelToCoords(sf::Vector2i(event.mouseButton.x, event.mouseButton.y));
            }
        } else if (event.type == sf::Event::MouseButtonReleased) {
            // Mouse button is released, no longer move
            if (event.mouseButton.button == 0) {
                moving = false;
            }
        } else if (event.type == sf::Event::MouseMoved) {
                // Ignore mouse movement unless a button is pressed (see above)
                if (!moving)
                    break;
                window.clear();
                // Determine the new position in world coordinates
                const sf::Vector2f newPos = window.mapPixelToCoords(sf::Vector2i(event.mouseMove.x, event.mouseMove.y));
                // Determine how the cursor has moved
                // Swap these to invert the movement direction
                const sf::Vector2f deltaPos = oldPos - newPos;

                // Move our view accordingly and update the window
                auto view = window.getView();
                view.setCenter(view.getCenter() + deltaPos);
                window.setView(view);

                // Save the new position as the old one
                // We're recalculating this, since we've changed the view
                oldPos = window.mapPixelToCoords(sf::Vector2i(event.mouseMove.x, event.mouseMove.y));
            }
    }
}

sf::Color Colors[5] = {sf::Color(40, 83, 107), sf::Color(236, 125, 16), sf::Color(144, 227, 154), sf::Color(157, 209, 241), sf::Color(201, 140, 167)};


int main() {
    Matrix2f m;
    m << 0.4, 0.2, -0.2, 0.4;

    Vector2f Offset1(0, 0);
    Vector2f Offset2(0, 1);
    Vector2f Offset3(-1, 0);
    Vector2f Offset4(1, 0);
    Vector2f Offset5(0, -1);
    Vector2f Offsets[5] = {Offset1, Offset2, Offset3, Offset4, Offset5};

    Vector2f base(0, 0);

    sf::VertexArray va(sf::PrimitiveType::Points, Max*5);
    
    sf::View view(sf::FloatRect(0, 0, Scale, Scale));

    sf::Transform tf;
    tf.translate(Scale/2, Scale/2);
    tf.scale(Scale/4, Scale/4);


    auto window = sf::RenderWindow(sf::VideoMode(Scale, Scale), "Fractal");
    window.setView(view);

    int count;

    while (window.isOpen()) {

        
        for (int count2=0; count2<Max; count2++) {
            manageEvents(window);
            base = m * base;
            count = 0;
            for (Vector2f offset : Offsets) {
                Vector2f point = base + offset;
                va[5*count2+count].position = {point[0], point[1]};
                va[5*count2+count].color = Colors[count];
                count++;
            }
            base = base + Offsets[dis(gen)];
        }

        

        // window.clear();
            
        window.draw(va, tf);
        window.display();
            




    }

    return 0;
}