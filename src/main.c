#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_VARS 100
#define MAX_VAR_NAME_LENGTH 50
#define MAX_STRING_LENGTH 256

// Estructura para almacenar las variables
typedef struct {
    char nombre[MAX_VAR_NAME_LENGTH];
    char valor[MAX_STRING_LENGTH];
} Variable;

// Array de variables
Variable variables[MAX_VARS];
int var_count = 0;

// Función para buscar una variable por nombre
int buscar_variable(const char *nombre) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(variables[i].nombre, nombre) == 0) {
            return i;
        }
    }
    return -1;
}

// Función para agregar o actualizar una variable
void agregar_variable(const char *nombre, const char *valor) {
    int idx = buscar_variable(nombre);
    if (idx == -1) {  // Si la variable no existe, la agregamos
        if (var_count < MAX_VARS) {
            strncpy(variables[var_count].nombre, nombre, MAX_VAR_NAME_LENGTH - 1);
            variables[var_count].nombre[MAX_VAR_NAME_LENGTH - 1] = '\0'; // Asegurar terminación
            strncpy(variables[var_count].valor, valor, MAX_STRING_LENGTH - 1);
            variables[var_count].valor[MAX_STRING_LENGTH - 1] = '\0'; // Asegurar terminación
            var_count++;
        } else {
            printf("Error: Se alcanzó el número máximo de variables\n");
        }
    } else {  // Si ya existe, actualizamos su valor
        strncpy(variables[idx].valor, valor, MAX_STRING_LENGTH - 1);
        variables[idx].valor[MAX_STRING_LENGTH - 1] = '\0'; // Asegurar terminación
    }
}

// Función para verificar si un nombre de variable es válido
int es_nombre_variable_valido(const char *nombre) {
    // Verificar que no esté vacío y que comience con una letra
    if (strlen(nombre) == 0 || !isalpha(nombre[0])) {
        return 0;
    }
    // Verificar que todos los caracteres sean letras o números
    for (size_t i = 0; i < strlen(nombre); i++) {
        if (!isalnum(nombre[i])) {
            return 0;
        }
    }
    return 1;
}

// Función para eliminar comentarios y espacios innecesarios
void eliminar_comentarios(char *linea) {
    char *comentario = strstr(linea, "!!");
    if (comentario != NULL) {
        *comentario = '\0';  // Terminar la cadena en el inicio del comentario
    }
}

// Función para interpretar una línea de código
void interpretar_linea(const char *linea) {
    // Copiar la línea para eliminar comentarios
    char linea_sin_comentarios[256];
    strncpy(linea_sin_comentarios, linea, sizeof(linea_sin_comentarios) - 1);
    linea_sin_comentarios[sizeof(linea_sin_comentarios) - 1] = '\0';
    
    eliminar_comentarios(linea_sin_comentarios);

    // Ignorar líneas vacías
    if (strlen(linea_sin_comentarios) == 0) {
        return;
    }

    // Ignorar START; y ENDED;
    if (strcmp(linea_sin_comentarios, "START;") == 0 || strcmp(linea_sin_comentarios, "ENDED;") == 0) {
        return;
    }

    if (strncmp(linea_sin_comentarios, "output(", 7) == 0) {
        char argumento[MAX_STRING_LENGTH];
        sscanf(linea_sin_comentarios, "output(%[^)]);", argumento);

        if (argumento[0] == '"') {  // Si es una cadena de texto
            argumento[strlen(argumento) - 1] = '\0';  // Quitamos la comilla final
            printf("%s\n", argumento + 1);  // Quitamos la comilla inicial y imprimimos
        } else {  // Si es una variable
            if (es_nombre_variable_valido(argumento)) {
                int idx = buscar_variable(argumento);
                if (idx != -1) {
                    printf("%s\n", variables[idx].valor);
                } else {
                    printf("Error: variable '%s' no definida\n", argumento);
                }
            } else {
                printf("Error: nombre de variable inválido '%s'\n", argumento);
            }
        }
    } else if (strstr(linea_sin_comentarios, "=>") != NULL) {
        char nombre[MAX_VAR_NAME_LENGTH];
        char valor[MAX_STRING_LENGTH];
        sscanf(linea_sin_comentarios, "%s => %255[^\n]", nombre, valor);

        if (es_nombre_variable_valido(nombre)) {
            agregar_variable(nombre, valor);
        } else {
            printf("Error: nombre de variable inválido '%s'\n", nombre);
        }
    } else if (strncmp(linea_sin_comentarios, "input(", 6) == 0) {
        char nombre[MAX_VAR_NAME_LENGTH];
        char valor[MAX_STRING_LENGTH];
        sscanf(linea_sin_comentarios, "input(%[^)]);", nombre);

        if (es_nombre_variable_valido(nombre)) {
            printf("Introduce el valor para la variable '%s': ", nombre);
            if (fgets(valor, sizeof(valor), stdin)) {
                valor[strcspn(valor, "\n")] = '\0'; // Eliminar el salto de línea del input
                agregar_variable(nombre, valor);
            } else {
                printf("Error al leer la entrada.\n");
            }
        } else {
            printf("Error: nombre de variable inválido '%s'\n", nombre);
        }
    } else {
        printf("Error: sintaxis no reconocida\n");
    }
}

// Función para leer e interpretar un archivo .asb
void leer_archivo(const char *nombre_archivo) {
    FILE *archivo = fopen(nombre_archivo, "r");
    if (archivo == NULL) {
        printf("Error: No se pudo abrir el archivo %s\n", nombre_archivo);
        exit(1);
    }

    char linea[256];
    while (fgets(linea, sizeof(linea), archivo)) {
        // Eliminar salto de línea al final
        linea[strcspn(linea, "\n")] = '\0';
        interpretar_linea(linea);
    }

    fclose(archivo);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <archivo.asb>\n", argv[0]);
        return 1;
    }

    // Verificar que el archivo tenga la extensión .asb
    char *nombre_archivo = argv[1];
    if (strstr(nombre_archivo, ".asb") == NULL) {
        printf("Error: Solo se pueden leer archivos con la extensión .asb\n");
        return 1;
    }

    // Leer e interpretar el archivo
    leer_archivo(nombre_archivo);

    return 0;
}
