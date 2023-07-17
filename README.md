# Gamify - Enhanced Game Recognition with Recommendations

![Game Classifier and Recommender](https://cdn.domestika.org/c_fit,dpr_auto,f_auto,q_80,t_base_params,w_820/v1606539120/content-items/006/327/049/SM-Videogame-original.png?1606539120)

Welcome to our Gamify project! This repository contains a powerful deep learning model that accurately classifies ten popular games and recommends similar games tailored to your preferences. Whether you are a fan of Among Us, Apex Legends, Fortnite, Forizon, Free Fire, Genshin Impact, God of War, Minecraft, Roblox, or Terraria, our model has got you covered!

## Features

- **Game Classification:** Our model has been trained on an extensive dataset of 10,000 images, allowing it to accurately classify the ten gaming titles mentioned above. Just provide an image of the game, and our model will tell you which game it belongs to!

- **Transfer Learning with ResNet-50:** The backbone of our classification model is the ResNet-50 transfer learning model. This state-of-the-art architecture empowers the model to achieve impressive training accuracy of 0.9 and validation accuracy of 0.92, ensuring reliable and consistent results.

- **Personalized Game Recommendations:** We understand that every gamer has unique tastes. That's why our recommender system combines both content-based and collaborative filtering approaches. We assign a weightage of 0.7 to content-based filtering, considering each game's attributes to make relevant suggestions. Additionally, a weightage of 0.3 is given to collaborative filtering, based on user preferences and behavior. Our database includes 20,000 similar games from IMDB, ensuring that the recommendations are tailor-made for you!

- **Web Application Deployment:** We have deployed our model in a web application using the FastAPI backend framework. The frontend is built with HTML, CSS, and JavaScript, creating a seamless and user-friendly experience. Just visit our website and start exploring different game categories or receive personalized game recommendations.

## How to Use

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Start the backend server using uvicorn: `uvicorn app:app --reload`.
   The backend server will be running at `http://127.0.0.1:8000`.

4. Open the `index.html` and run the file in your web browser to access the website.

5. Use the provided script to classify images of the ten games or make personalized game recommendations.

## Contributing

We welcome contributions from the community to improve our Game Classifier and Recommender. If you have any ideas, bug fixes, or additional features, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

We hope you enjoy using our Gamify! If you have any questions or need assistance, please don't hesitate to contact us. Happy gaming!

**Author:** Abhinav Reddy Gutha  
**Contact:** abhinavreddygutha@gmail.com 

