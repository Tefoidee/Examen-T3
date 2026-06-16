laberinto = [
    ['F',  1,  1,  1,  0,  1,  1,  1,  1],
    [ -2,  0,  0, -1,  0,  1,  0,  1,  0],
    [  1,  1,  0,  1,  1,  1,  0,  1,  0],
    [  0,  1,  0, -1,  0,  0,  0, -1,  0],
    [  1,  1,  1,  1,  1,  1,  1,  1,  0],
    [ -1,  0,  0,  0,  0,  0,  0,  1,  1],
    [  1,  1,  1,  1, -1, -1,  1,  1,  0],
    [  1,  0,  0,  1,  0,  1,  0,  1,  0],
    ['I',  1, -1,  1,  1,  1,  0,  1,  1],
]

FILAS           = 9
COLS            = 9
VIDAS_INICIALES = 3
META            = (0, 0)
INICIO          = (8, 0)

MOVS    = [(1, 0), (0, 1), (-1, 0), (0, -1)]
NOMBRES = ['Abajo', 'Derecha', 'Arriba', 'Izquierda']

todas_soluciones = []   # guarda todos los caminos encontrados


def costo(celda):
    if celda in ('I', 'F', 1):
        return 0
    return celda


def imprimir_laberinto_con_camino(titulo, camino):
    cs = set(camino)
    print(f"\n{titulo}")
    print("      " + "".join(f"{c:>4}" for c in range(COLS)))
    print("      " + "-" * (COLS * 4))
    for i, fila in enumerate(laberinto):
        linea = f" {i:2d} |"
        for j, celda in enumerate(fila):
            if (i, j) in cs:
                linea += f"{'*':>4}"
            else:
                linea += f"{str(celda):>4}"
        print(linea)
    print()


def backtracking(fila, col, vidas, camino, visitado):
    """Busca TODAS las soluciones, sin detenerse en la primera."""
    camino.append((fila, col))

    if (fila, col) == META:
        # Guardar copia de este camino como solución
        todas_soluciones.append(list(camino))
        camino.pop()
        return   # continúa buscando más soluciones

    for (df, dc), nombre in zip(MOVS, NOMBRES):
        nf, nc = fila + df, col + dc

        if not (0 <= nf < FILAS and 0 <= nc < COLS):
            continue
        if visitado[nf][nc]:
            continue

        celda = laberinto[nf][nc]
        if celda == 0:
            continue

        nuevas_vidas = vidas + costo(celda)
        if nuevas_vidas < 0:
            continue

        visitado[nf][nc] = True
        backtracking(nf, nc, nuevas_vidas, camino, visitado)
        visitado[nf][nc] = False

    camino.pop()


def mostrar_camino_detalle(num, camino):
    print(f"\n{'─'*64}")
    print(f"  SOLUCIÓN {num}  —  {len(camino)} pasos")
    print(f"{'─'*64}")
    vv = VIDAS_INICIALES
    for paso, (r, c) in enumerate(camino):
        celda = laberinto[r][c]
        vv += costo(celda)
        marca = "⚠" if vv == 0 else " "
        print(f"  {marca} Paso {paso+1:2d}: fila={r}  col={c}"
              f"  celda={str(celda):>3}  vidas = {vv}")
    imprimir_laberinto_con_camino(f"Laberinto — Solución {num} (camino = *):", camino)
    print(f"  Matriz de salida — Solución {num}:\n")
    cs = set(camino)
    for i, fila in enumerate(laberinto):
        linea = ""
        for j, celda in enumerate(fila):
            if (i, j) in cs:
                linea += f"{'*':>4}"
            else:
                linea += f"{str(celda):>4}"
        print(linea)


def main():
    print("=" * 64)
    print("   LABERINTO — TODAS LAS SOLUCIONES  |  COMP1303A")
    print("   Inicio : (I) fila 8, col 0   →   Meta : (F) fila 0, col 0")
    print("   Vidas  : 3 iniciales  |  inviable si vidas < 0")
    print("=" * 64)

    # Mostrar laberinto original
    print("\nLABERINTO ORIGINAL:")
    print("      " + "".join(f"{c:>4}" for c in range(COLS)))
    print("      " + "-" * (COLS * 4))
    for i, fila in enumerate(laberinto):
        linea = f" {i:2d} |"
        for j, celda in enumerate(fila):
            linea += f"{str(celda):>4}"
        print(linea)

    # Ejecutar backtracking buscando TODAS las soluciones
    visitado = [[False] * COLS for _ in range(FILAS)]
    fi, ci = INICIO
    visitado[fi][ci] = True
    backtracking(fi, ci, VIDAS_INICIALES, [], visitado)

    print(f"\n{'='*64}")
    if not todas_soluciones:
        print("  ❌  NO SE ENCONTRÓ NINGUNA SOLUCIÓN VIABLE")
    else:
        print(f"  ✅  SE ENCONTRARON {len(todas_soluciones)} SOLUCIÓN(ES)")
        print(f"{'='*64}")
        for i, camino in enumerate(todas_soluciones, 1):
            mostrar_camino_detalle(i, camino)

    print(f"\n{'='*64}")
    print(f"  RESUMEN FINAL")
    print(f"{'='*64}")
    for i, camino in enumerate(todas_soluciones, 1):
        vv = VIDAS_INICIALES
        for r, c in camino:
            vv += costo(laberinto[r][c])
        print(f"  Solución {i}: {len(camino)} pasos | vidas restantes = {vv}")
    print(f"{'='*64}\n")


if __name__ == "__main__":
    main()