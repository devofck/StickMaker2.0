import matplotlib.pyplot as plt


def draw_graph(users: int, sets: int) -> None:
    x = ['Пользователи', 'Наборы']
    y = [users, sets]
    coefficient = round(sets / users * 100, 2)
    plt.figure(figsize=(16, 10))
    plt.xticks(fontsize=35)
    plt.yticks(fontsize=30)
    plt.text(0.25, -0.55, "коэф: " + str(coefficient) + '%', fontsize=30, color='red')
    plt.bar(x=x, height=y)
    plt.title("Соотношение количества пользователей и наборов", fontsize=40, color="blue")

    plt.savefig('stats.png', dpi=300)


