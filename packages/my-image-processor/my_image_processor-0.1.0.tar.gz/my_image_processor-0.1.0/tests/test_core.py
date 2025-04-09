import os
from img_processor.core import resize_image

def test_resize_image(tmp_path):
    # Cria um caminho temporário para os arquivos de teste
    input_path = tmp_path / "input.jpg"
    output_path = tmp_path / "output.jpg"
    
    # Cria uma imagem de teste (pode ser uma imagem simples)
    from PIL import Image
    img = Image.new("RGB", (200, 200), color="blue")
    img.save(input_path)
    
    # Redimensiona a imagem para 100x100
    resize_image(str(input_path), str(output_path), (100, 100))
    
    # Verifica se o arquivo de saída foi criado
    assert os.path.exists(output_path)
    # Opcionalmente, você pode abrir a imagem para verificar o tamanho
    with Image.open(output_path) as im_out:
        assert im_out.size == (100, 100)
