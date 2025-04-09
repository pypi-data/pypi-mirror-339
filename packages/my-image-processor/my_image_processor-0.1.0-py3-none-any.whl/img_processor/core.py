from PIL import Image

def resize_image(input_path, output_path, size):
    """
    Redimensiona uma imagem para o tamanho especificado.
    
    Parâmetros:
      input_path: Caminho da imagem de entrada.
      output_path: Caminho para salvar a imagem processada.
      size: Nova dimensão da imagem, no formato (largura, altura).
    """
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)
