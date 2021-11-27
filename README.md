# Sistema de recomendación

## Uso

Para ejecutar el programa se ejecuta:

 ```$ python Recomendacion.py [Matriz de utilidad] [Métrica elegida] [Número de vecinos] [Tipo de predicción]```

Posibles valores de los argumentos:
- **Matriz de utilizad**: Cualquier fichero de texto que contenga una matriz con el formato adecuado.
- **Métrica**: [pearson/cosine_distance/euclidean_distance]
- **Número de vecinos**: Cualquier número mayor que 2.
- **Tipo de predicción**: [simple/mean_diff]