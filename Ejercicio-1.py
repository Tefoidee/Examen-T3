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

todas_soluciones = []


def costo(celda):
    """
    I → suma 1 vida (al inicio del recorrido)
    F → paso libre (es la meta, no suma ni quita)
    1 → paso libre (0)
    -1 → quita 1 vida
    -2 → quita 2 vidas
    """
    if celda == 'I':
        return 1    # suma 1 al pisar la salida
    if celda in ('F', 1):
        return 0    # paso libre
    return celda    # -1 o -2


def imprimir_laberinto_original():
    print("\nLABERINTO ORIGINAL:")
    print("      " + "".join(f"{c:>4}" for c in range(COLS)))
    print("      " + "-" * (COLS * 4))
    for i, fila in enumerate(laberinto):
        linea = f" {i:2d} |"
        for j, celda in enumerate(fila):
            linea += f"{str(celda):>4}"
        print(linea)
    print()


def imprimir_con_camino(titulo, camino):
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
    """Busca TODAS las soluciones sin detenerse en la primera."""
    camino.append((fila, col))

    if (fila, col) == META:
        todas_soluciones.append((list(camino), vidas))
        camino.pop()
        return

    for (df, dc) in MOVS:
        nf, nc = fila + df, col + dc

        if not (0 <= nf < FILAS and 0 <= nc < COLS):
            continue
        if visitado[nf][nc]:
            continue

        celda = laberinto[nf][nc]
        if celda == 0:
            continue

        nuevas_vidas = vidas + costo(celda)
        if nuevas_vidas <= 0:
            continue

        visitado[nf][nc] = True
        backtracking(nf, nc, nuevas_vidas, camino, visitado)
        visitado[nf][nc] = False

    camino.pop()


def mostrar_solucion(num, camino, vidas_finales):
    print(f"\n{'─'*64}")
    print(f"  SOLUCIÓN {num}  —  {len(camino)} pasos  |  "
          f"vidas al llegar a F: {vidas_finales}")
    print(f"{'─'*64}")

    vv = VIDAS_INICIALES
    for paso, (r, c) in enumerate(camino):
        celda = laberinto[r][c]
        vv += costo(celda)
        print(f"    Paso {paso+1:2d}: fila={r}  col={c}"
              f"  celda={str(celda):>3}  vidas = {vv}")

    imprimir_con_camino(f"Laberinto — Solución {num} (camino = *):", camino)

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
    print("   I suma 1 vida al inicio  |  vidas iniciales: 3 → parte con 4")
    print("   Inviable si vidas <= 0")
    print("=" * 64)

    imprimir_laberinto_original()

    # Al pisar I el ratón tiene 3+1 = 4 vidas
    vidas_inicio = VIDAS_INICIALES + costo(laberinto[INICIO[0]][INICIO[1]])
    visitado = [[False] * COLS for _ in range(FILAS)]
    visitado[INICIO[0]][INICIO[1]] = True
    backtracking(INICIO[0], INICIO[1], vidas_inicio, [], visitado)

    print(f"\n{'='*64}")
    if not todas_soluciones:
        print("  ❌  NO SE ENCONTRÓ NINGUNA SOLUCIÓN VIABLE")
    else:
        print(f"  ✅  SE ENCONTRARON {len(todas_soluciones)} SOLUCIÓN(ES)")
        print(f"{'='*64}")
        for i, (camino, vidas_finales) in enumerate(todas_soluciones, 1):
            mostrar_solucion(i, camino, vidas_finales)

    print(f"\n{'='*64}")
    print(f"  RESUMEN FINAL")
    print(f"{'─'*64}")
    for i, (camino, vidas_finales) in enumerate(todas_soluciones, 1):
        print(f"  Solución {i}: {len(camino):2d} pasos  |  "
              f"vidas restantes al llegar = {vidas_finales}")
    print(f"{'='*64}\n")


if __name__ == "__main__":
    main()