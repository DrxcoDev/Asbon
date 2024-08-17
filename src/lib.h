#ifndef SIMPLE_LANG_H
#define SIMPLE_LANG_H

#include <stddef.h>  // Para size_t

#define MAX_VARS 100
#define MAX_VAR_NAME_LENGTH 50
#define MAX_STRING_LENGTH 256

// Estructura para almacenar las variables
typedef struct {
    char nombre[MAX_VAR_NAME_LENGTH];
    char valor[MAX_STRING_LENGTH];
} Variable;

// Función para buscar una variable por nombre
int buscar_variable(const char *nombre);

// Función para agregar o actualizar una variable
void agregar_variable(const char *nombre, const char *valor);

// Función para verificar si un nombre de variable es válido
int es_nombre_variable_valido(const char *nombre);

// Función para eliminar comentarios y espacios innecesarios
void eliminar_comentarios(char *linea);

// Función para interpretar una línea de código
void interpretar_linea(const char *linea);

// Función para leer e interpretar un archivo .asb
void leer_archivo(const char *nombre_archivo);

// Función para iniciar la ejecución desde una biblioteca compartida
__attribute__((visibility("default"))) void ejecutar_archivo(const char *nombre_archivo);

#endif // SIMPLE_LANG_H
