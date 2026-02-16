import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle

def check_zone(x, y):
    """Проверяет, к какой зоне принадлежит точка (x,y)"""
    # Условия для фигур
    inside_circle = x**2 + y**2 <= 16  # круг радиусом 4
    inside_square = abs(x) <= 5 and abs(y) <= 5  # квадрат от -5 до 5
    
    # Уравнения прямых (диагоналей квадрата)
    # Прямая 1: от (-5,5) до (5,-5) -> y = -x
    # Прямая 2: от (5,5) до (-5,-5) -> y = x
    
    # Определяем положение относительно прямых
    above_line1 = y > -x  # больше прямой 1
    below_line1 = y < -x  # меньше прямой 1
    above_line2 = y > x   # больше прямой 2
    below_line2 = y < x   # меньше прямой 2
    
    # Проверяем условия для каждой зоны
    if below_line1 and above_line2 and inside_circle:
        return 1
    elif above_line1 and below_line2 and inside_circle:
        return 2
    elif above_line1 and above_line2 and not inside_circle and inside_square:
        return 3
    elif below_line1 and below_line2 and not inside_circle and inside_square:
        return 4
    else:
        return 0  # точка не принадлежит ни одной зоне

def onclick(event):
    """Обработчик клика мыши"""
    x, y = event.xdata, event.ydata
    
    if x is not None and y is not None:
        # Определяем зону
        zone = check_zone(x, y)
        
        # Очищаем предыдущие аннотации
        for text in ax.texts:
            text.remove()
        
        # Удаляем предыдущую точку
        if hasattr(onclick, 'point'):
            onclick.point.remove()
        
        # Добавляем новую аннотацию и точку
        if zone > 0:
            colors = ['', 'red', 'blue', 'green', 'orange']
            zone_names = ['', 'Зона 1', 'Зона 2', 'Зона 3', 'Зона 4']
            color = colors[zone]
            message = f'Точка ({x:.2f}, {y:.2f}) в {zone_names[zone]}'
            
            onclick.point = ax.plot(x, y, 'o', color=color, markersize=8, 
                                   markeredgecolor='black', zorder=5)[0]
        else:
            color = 'gray'
            message = f'Точка ({x:.2f}, {y:.2f}) вне целевых зон'
            onclick.point = ax.plot(x, y, 'o', color=color, markersize=8, 
                                   markeredgecolor='black', zorder=5)[0]
        
        ax.text(0, -6.5, message, fontsize=12, color=color, 
                ha='center', va='center', transform=ax.transData,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.2))
        
        plt.draw()

# Создаем фигуру и оси
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

# Устанавливаем пределы осей
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)

# Добавляем сетку
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)

# Рисуем квадрат
square = Rectangle((-5, -5), 10, 10, fill=False, color='black', linewidth=2, label='Квадрат')
ax.add_patch(square)

# Рисуем круг
circle = Circle((0, 0), 4, fill=False, color='blue', linewidth=2, label='Круг R=4')
ax.add_patch(circle)

# Рисуем диагонали квадрата
x_vals = np.array([-5, 5])
# Прямая 1: от (-5,5) до (5,-5) -> y = -x
ax.plot(x_vals, -x_vals, 'r--', linewidth=2, label='Прямая 1 (y=-x)')
# Прямая 2: от (5,5) до (-5,-5) -> y = x
ax.plot(x_vals, x_vals, 'g--', linewidth=2, label='Прямая 2 (y=x)')

# Закрашиваем зоны разными цветами для наглядности
x = np.linspace(-5, 5, 300)
y = np.linspace(-5, 5, 300)
X, Y = np.meshgrid(x, y)

# Создаем маски для каждой зоны
Z1 = (Y < -X) & (Y > X) & (X**2 + Y**2 <= 16)
Z2 = (Y > -X) & (Y < X) & (X**2 + Y**2 <= 16)
Z3 = (Y > -X) & (Y > X) & (X**2 + Y**2 > 16) & (np.abs(X) <= 5) & (np.abs(Y) <= 5)
Z4 = (Y < -X) & (Y < X) & (X**2 + Y**2 > 16) & (np.abs(X) <= 5) & (np.abs(Y) <= 5)

# Отображаем зоны с прозрачной заливкой
ax.contourf(X, Y, Z1, levels=[0.5, 1], colors=['red'], alpha=0.2)
ax.contourf(X, Y, Z2, levels=[0.5, 1], colors=['blue'], alpha=0.2)
ax.contourf(X, Y, Z3, levels=[0.5, 1], colors=['green'], alpha=0.2)
ax.contourf(X, Y, Z4, levels=[0.5, 1], colors=['orange'], alpha=0.2)

# Добавляем подписи зон
ax.text(-3, 0, 'Зона 1', fontsize=12, color='red', ha='center', va='center', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.3))
ax.text(3, 0, 'Зона 2', fontsize=12, color='blue', ha='center', va='center', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='blue', alpha=0.3))
ax.text(0, 3, 'Зона 3', fontsize=12, color='green', ha='center', va='center', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='green', alpha=0.3))
ax.text(0, -3, 'Зона 4', fontsize=12, color='orange', ha='center', va='center', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='orange', alpha=0.3))

# Настройки графика
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Четыре зоны: квадрат, круг и диагонали\n(Кликните для проверки точки)')
ax.legend(loc='upper right')

# Подключаем обработчик клика
fig.canvas.mpl_connect('button_press_event', onclick)

plt.tight_layout()
plt.show()