class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def create_tree():
    print("\nСоздание дерева:")
    print("Введите значение корня дерева:")
    root_value = int(input())
    root = Node(root_value)
    
    nodes = [root]
    level = 0
    
    while nodes:
        level_nodes = []
        print(f"\nУровень {level}:")
        
        for current in nodes:
            print(f"\nДля узла со значением {current.value}:")
            
            # левое
            left_input = input("Введите значение левого потомка (или 'n' если его нет): ")
            if left_input.lower() != 'n':
                current.left = Node(int(left_input))
                level_nodes.append(current.left)
            
            # правое
            right_input = input("Введите значение правого потомка (или 'n' если его нет): ")
            if right_input.lower() != 'n':
                current.right = Node(int(right_input))
                level_nodes.append(current.right)
        
        nodes = level_nodes
        level += 1
        
        continue_input = input("\nХотите добавить следующий уровень? (y/n): ")
        if continue_input.lower() != 'y':
            break
            
    return root

def is_anagram_tree(root):
    def is_mirror(left, right):
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (left.value == right.value and 
                is_mirror(left.left, right.right) and 
                is_mirror(left.right, right.left))
    
    return is_mirror(root.left, root.right)

def print_tree(root, level=0, prefix="Корень: "):
    if root is not None:
        print("  " * level + prefix + str(root.value))
        if root.left or root.right:
            if root.left:
                print_tree(root.left, level + 1, "Л: ")
            if root.right:
                print_tree(root.right, level + 1, "П: ")

def main():
    while True:
        print("\n1. Создать новое дерево")
        print("2. Выйти")
        
        choice = input("\nВыберите действие (1-2): ")
        
        if choice == '1':
            tree = create_tree()
            if tree:
                print("\nСозданное дерево:")
                print_tree(tree)
                print("\nРезультат проверки на анаграмму:", is_anagram_tree(tree))
        elif choice == '2':
            print("Программа завершена")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()





