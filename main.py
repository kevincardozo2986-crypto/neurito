from pathlib import Path

import numpy as np
import pygame

LANGUAGE = "en"  # Change to "es" for Spanish interface text.
TEXT = {
    "en": {
        "title": "NEURITO - MY ARTIFICIAL BRAIN",
        "hunger": "Hunger", "energy": "Energy", "boredom": "Boredom",
        "eat": "EAT", "sleep": "SLEEP", "play": "PLAY", "neutral": "CALM",
        "accuracy": "Test accuracy against synthetic policy",
        "epoch": "Epoch", "loss": "Loss",
        "controls1": "H/J: hunger +/-    E/D: energy +/-",
        "controls2": "A/S: boredom +/-    R: random",
        "controls3": "N: calm state    ESC: quit",
    },
    "es": {
        "title": "NEURITO - MI CEREBRO ARTIFICIAL",
        "hunger": "Hambre", "energy": "Energía", "boredom": "Aburrimiento",
        "eat": "COMER", "sleep": "DORMIR", "play": "JUGAR", "neutral": "NEUTRAL",
        "accuracy": "Precisión frente a la política sintética",
        "epoch": "Época", "loss": "Pérdida",
        "controls1": "H/J: hambre +/-    E/D: energía +/-",
        "controls2": "A/S: aburrimiento +/-    R: aleatorio",
        "controls3": "N: estado tranquilo    ESC: salir",
    },
}
labels = TEXT[LANGUAGE]
actions = ("eat", "sleep", "play")
HIDDEN_NEURONS = 6
EPOCHS = 1200
LEARNING_RATE = 0.1
print(f"\nConfiguracion: {HIDDEN_NEURONS} neuronas ocultas | "
      f"{EPOCHS} epocas | tasa {LEARNING_RATE}")

# Synthetic examples follow a simple priority policy.
np.random.seed(42)
X = np.random.rand(3000, 3)
targets = np.argmax(np.column_stack((X[:, 0], 1 - X[:, 1], X[:, 2])), axis=1)
W1 = np.random.randn(3, HIDDEN_NEURONS) * 0.5
b1 = np.zeros((1, HIDDEN_NEURONS))
W2 = np.random.randn(HIDDEN_NEURONS, 3) * 0.5
b2 = np.zeros((1, 3))


def relu(values):
    return np.maximum(0, values)


def softmax(values):
    exp_values = np.exp(values - np.max(values, axis=1, keepdims=True))
    return exp_values / np.sum(exp_values, axis=1, keepdims=True)


def predict(data):
    hidden = relu(data @ W1 + b1)
    return softmax(hidden @ W2 + b2)


# Full-batch gradient descent.
for epoch in range(EPOCHS):
    z1 = X @ W1 + b1
    hidden = relu(z1)
    probabilities = softmax(hidden @ W2 + b2)
    count = len(X)
    loss = -np.mean(np.log(probabilities[np.arange(count), targets] + 1e-10))
    delta2 = probabilities.copy()
    delta2[np.arange(count), targets] -= 1
    delta2 /= count
    grad_W2 = hidden.T @ delta2
    grad_b2 = np.sum(delta2, axis=0, keepdims=True)
    delta1 = (delta2 @ W2.T) * (z1 > 0)
    grad_W1 = X.T @ delta1
    grad_b1 = np.sum(delta1, axis=0, keepdims=True)
    W1 -= LEARNING_RATE * grad_W1
    b1 -= LEARNING_RATE * grad_b1
    W2 -= LEARNING_RATE * grad_W2
    b2 -= LEARNING_RATE * grad_b2
    if epoch % 200 == 0:
        print(f"{labels['epoch']} {epoch} | {labels['loss']}: {loss:.4f}")

test = np.random.RandomState(123).rand(1000, 3)
test_targets = np.argmax(
    np.column_stack((test[:, 0], 1 - test[:, 1], test[:, 2])), axis=1
)
accuracy = np.mean(np.argmax(predict(test), axis=1) == test_targets)
print(f"{labels['accuracy']}: {accuracy:.2%}")
final_probabilities = predict(X)
final_loss = -np.mean(np.log(final_probabilities[np.arange(len(X)), targets] + 1e-10))
print(f"Perdida final de entrenamiento: {final_loss:.4f}")


def print_prediction(values):
    scores = predict(np.array([values]))[0]
    names = ("COMER", "DORMIR", "JUGAR")
    print(f"Hambre={values[0]:.3f} Energia={values[1]:.3f} "
          f"Aburrimiento={values[2]:.3f} -> {names[int(np.argmax(scores))]} | "
          + " | ".join(f"{name}: {score:.2%}" for name, score in zip(names, scores)))


print("\nExperimento: variar hambre con energia=0.6 y aburrimiento=0.2")
for hunger in (0.2, 0.39, 0.4, 0.41, 0.6):
    print_prediction([hunger, 0.6, 0.2])
print("\nExperimento: prioridades casi identicas (Softmax)")
for values in ([0.5, 0.5, 0.5], [0.501, 0.5, 0.5],
               [0.5, 0.499, 0.5], [0.5, 0.5, 0.501]):
    print_prediction(values)
print("\nExperimento 1: fronteras de decision (pasos de 0.001)")
for column, base, description in (
    (0, [0, 0.6, 0.2], "Hambre; energia=0.6, aburrimiento=0.2"),
    (1, [0.4, 0, 0.2], "Energia; hambre=0.4, aburrimiento=0.2"),
    (2, [0.4, 0.7, 0], "Aburrimiento; hambre=0.4, energia=0.7"),
):
    print(description)
    previous = None
    for value in np.linspace(0, 1, 1001):
        values = base.copy()
        values[column] = value
        current = int(predict(np.array([values])).argmax())
        if current != previous:
            print_prediction(values)
            previous = current


def train_experiment(width, epochs, rate, fourth_action=False):
    """Entrena una red independiente sin alterar la mascota ni su modelo."""
    rng = np.random.RandomState(42)
    data = rng.rand(3000, 3)
    training_targets = targets.copy()
    evaluation_targets = test_targets.copy()
    outputs = 4 if fourth_action else 3
    if fourth_action:
        for inputs, output_targets in ((data, training_targets), (test, evaluation_targets)):
            calm = (inputs[:, 0] < 0.4) & (inputs[:, 1] > 0.6) & (inputs[:, 2] < 0.4)
            output_targets[calm] = 3
    weights1 = rng.randn(3, width) * 0.5
    bias1 = np.zeros((1, width))
    weights2 = rng.randn(width, outputs) * 0.5
    bias2 = np.zeros((1, outputs))
    history = []

    def probabilities_for(inputs):
        return softmax(relu(inputs @ weights1 + bias1) @ weights2 + bias2)

    for step in range(epochs):
        z = data @ weights1 + bias1
        hidden_values = relu(z)
        probabilities = softmax(hidden_values @ weights2 + bias2)
        if step % 200 == 0:
            history.append((step, -np.mean(np.log(
                probabilities[np.arange(len(data)), training_targets] + 1e-10))))
        delta = probabilities.copy()
        delta[np.arange(len(data)), training_targets] -= 1
        delta /= len(data)
        hidden_delta = (delta @ weights2.T) * (z > 0)
        weights2 -= rate * hidden_values.T @ delta
        bias2 -= rate * delta.sum(axis=0, keepdims=True)
        weights1 -= rate * data.T @ hidden_delta
        bias1 -= rate * hidden_delta.sum(axis=0, keepdims=True)

    training_probabilities = probabilities_for(data)
    evaluation_probabilities = probabilities_for(test)
    training_loss = -np.mean(np.log(
        training_probabilities[np.arange(len(data)), training_targets] + 1e-10))
    evaluation_loss = -np.mean(np.log(
        evaluation_probabilities[np.arange(len(test)), evaluation_targets] + 1e-10))
    predicted = evaluation_probabilities.argmax(axis=1)
    print(f"{width:>8} {epochs:>7} {rate:>7g} {training_loss:>13.4f} "
          f"{evaluation_loss:>13.4f} {np.mean(predicted == evaluation_targets):>11.2%}")
    if fourth_action:
        print("Etiquetas: 0=COMER, 1=DORMIR, 2=JUGAR, 3=NEUTRAL")
        print("Neutral: hambre<0.4, energia>0.6 y aburrimiento<0.4")
        for index, name in enumerate(("COMER", "DORMIR", "JUGAR", "NEUTRAL")):
            mask = evaluation_targets == index
            recall = np.mean(predicted[mask] == index) if mask.any() else float('nan')
            print(f"  {name}: {mask.sum()} ejemplos de prueba; acierto por clase={recall:.2%}")
        for values in ([0.2, 0.9, 0.2], [0.8, 0.9, 0.2],
                       [0.2, 0.1, 0.2], [0.2, 0.9, 0.8]):
            scores = probabilities_for(np.array([values]))[0]
            print(f"  Entrada {values}: " + " | ".join(
                f"{name}={score:.2%}" for name, score in zip(
                    ("COMER", "DORMIR", "JUGAR", "NEUTRAL"), scores)))
    return history


table_header = "Neuronas  Epocas    Tasa Perdida train Perdida prueba   Precision"
print("\nExperimento 3: comparar neuronas ocultas")
print("Mismos datos de entrenamiento y prueba; semilla 42. Una ejecucion por configuracion.")
print(table_header)
for width in (3, 6, 10, 20):
    train_experiment(width, 1200, 0.1)

print("\nExperimento 4: comparar epocas")
print(table_header)
for epochs in (200, 1200, 3000):
    train_experiment(6, epochs, 0.1)
print("\nExperimento 4: comparar tasas de aprendizaje")
print(table_header)
for rate in (0.01, 0.1, 1.0, 10.0):
    history = train_experiment(6, 1200, rate)
    print("  Evolucion de perdida: " + " -> ".join(
        f"epoca {step}: {value:.4f}" for step, value in history))

print("\nExperimento 5: cuarta accion aprendida (NEUTRAL)")
print(table_header)
train_experiment(6, 1200, 0.1, fourth_action=True)
print("\nFin de los experimentos. La ventana usa el modelo original de tres acciones.")

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Neurito")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 23)
asset_dir = Path(__file__).resolve().parent / "assets"
pet_size = (330, 330)


def load_frames(names):
    return [
        pygame.transform.smoothscale(
            pygame.image.load(str(asset_dir / name)).convert_alpha(), pet_size
        )
        for name in names
    ]


frames = {
    "neutral": load_frames(["neutral_1.png", "neutral_2.png", "neutral_3.png"]),
    "eat": load_frames(["comer_1.png", "comer_2.png"]),
    "sleep": load_frames(["dormir_1.png", "dormir_2.png"]),
    "play": load_frames(["jugar_1.png", "jugar_2.png"]),
}
needs = [0.2, 0.9, 0.2]
current_state = "neutral"
frame_index = 0
last_frame_time = pygame.time.get_ticks()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_h:
                needs[0] = min(1, needs[0] + 0.1)
            elif event.key == pygame.K_j:
                needs[0] = max(0, needs[0] - 0.1)
            elif event.key == pygame.K_e:
                needs[1] = min(1, needs[1] + 0.1)
            elif event.key == pygame.K_d:
                needs[1] = max(0, needs[1] - 0.1)
            elif event.key == pygame.K_a:
                needs[2] = min(1, needs[2] + 0.1)
            elif event.key == pygame.K_s:
                needs[2] = max(0, needs[2] - 0.1)
            elif event.key == pygame.K_r:
                needs = list(np.random.rand(3))
            elif event.key == pygame.K_n:
                needs = [0.2, 0.9, 0.2]

    probabilities = predict(np.array([needs]))[0]
    action = actions[int(np.argmax(probabilities))]
    if needs[0] < 0.4 and needs[1] > 0.6 and needs[2] < 0.4:
        state = "neutral"  # Display rule; the network has three outputs.
    else:
        state = action

    now = pygame.time.get_ticks()
    if state != current_state:
        current_state, frame_index, last_frame_time = state, 0, now
    elif now - last_frame_time >= 500:
        frame_index = (frame_index + 1) % len(frames[state])
        last_frame_time = now

    screen.fill((250, 245, 252))
    title = font.render(labels["title"], True, (55, 45, 75))
    screen.blit(title, (45, 28))
    colors = [(235, 125, 75), (70, 175, 115), (105, 125, 225)]
    for index, key in enumerate(("hunger", "energy", "boredom")):
        value = needs[index]
        y = 125 + index * 95
        text = small_font.render(
            f"{labels[key]}: {value * 100:.0f}%", True, (35, 40, 55)
        )
        screen.blit(text, (50, y - 27))
        pygame.draw.rect(screen, (215, 220, 230), (50, y, 290, 22), border_radius=7)
        pygame.draw.rect(
            screen, colors[index], (50, y, int(290 * value), 22), border_radius=7
        )

    pet = frames[state][frame_index]
    screen.blit(pet, pet.get_rect(center=(650, 235)))
    screen.blit(font.render(labels[state], True, (65, 50, 85)), (585, 420))
    for index, action_name in enumerate(actions):
        score = small_font.render(
            f"{labels[action_name]}: {probabilities[index] * 100:.1f}%",
            True, (55, 50, 75)
        )
        screen.blit(score, (50, 390 + index * 28))

    screen.blit(small_font.render(labels["controls1"], True, (70, 70, 90)), (50, 495))
    screen.blit(small_font.render(labels["controls2"], True, (70, 70, 90)), (50, 525))
    screen.blit(small_font.render(labels["controls3"], True, (70, 70, 90)), (50, 555))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
