import osmnx as ox

# Скачиваем граф по названию города
G = ox.graph_from_place('Бишкек, Кыргызстан', network_type='drive')
# Сохраняем в файл для последующего использования
ox.save_graphml(G, 'bishkek_road_network.graphml')