laberinto = [
    ['F',  1,  1,  1,  0,  1,  1,  1,  1],   # fila 0  (superior)
    [ -2,  0,  0, -1,  0,  1,  0,  1,  0],   # fila 1
    [  1,  1,  0,  1,  1,  1,  0,  1,  0],   # fila 2
    [  0,  1,  0, -1,  0,  0,  0, -1,  0],   # fila 3
    [  1,  1,  1,  1,  1,  1,  1,  1,  0],   # fila 4
    [ -1,  0,  0,  0,  0,  0,  0,  1,  1],   # fila 5
    [  1,  1,  1,  1, -1, -1,  1,  1,  0],   # fila 6
    [  1,  0,  0,  1,  0,  1,  0,  1,  0],   # fila 7
    ['I',  1, -1,  1,  1,  1,  0,  1,  1],   # fila 8  (inferior)
]

FILAS           = 9
COLS            = 9
VIDAS_INICIALES = 3
META            = (0, 0)
INICIO          = (8, 0)

# Orden: abajo, derecha, arriba, izquierda
MOVS    = [(1, 0), (0, 1), (-1, 0), (0, -1)]
NOMBRES = ['Abajo', 'Derecha', 'Arriba', 'Izquierda']


def costo(celda):
    """Retorna el costo de entrar a la celda (0, -1 o -2)."""
    if celda in ('I', 'F', 1):
        return 0
    return celda  # -1 o -2


def imprimir_laberinto(titulo, camino_set=None):
    cs = camino_set or set()
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
    """
    Estamos en (fila, col) con `vidas` actuales.
    Agrega la celda al camino, intenta avanzar; si falla retrocede.
    Condición inviable: vidas < 0  (quedar en 0 es sobrevivir por un pelo)
    """
    camino.append((fila, col))

    # Caso base: llegamos a F
    if (fila, col) == META:
        return True

    for (df, dc), nombre in zip(MOVS, NOMBRES):
        nf, nc = fila + df, col + dc

        # Verificar límites
        if not (0 <= nf < FILAS and 0 <= nc < COLS):
            continue
        if visitado[nf][nc]:
            continue

        celda = laberinto[nf][nc]
        if celda == 0:          # bloqueada
            continue

        nuevas_vidas = vidas + costo(celda)

        # Camino inviable si vidas caen a negativo
        if nuevas_vidas < 0:
            continue

        print(f"  → {nombre:10s}: ({fila},{col}) ➜ ({nf},{nc})"
              f"  celda={str(celda):>3}  vidas: {vidas} → {nuevas_vidas}")

        visitado[nf][nc] = True
        if backtracking(nf, nc, nuevas_vidas, camino, visitado):
            return True

        visitado[nf][nc] = False
        print(f"  ↩ Retrocede de ({nf},{nc}) a ({fila},{col})")

    camino.pop()
    return False


def main():
    print("=" * 64)
    print("   LABERINTO CON BACKTRACKING  —  COMP1303A")
    print("   Inicio : esquina inferior-izquierda  (I) = fila 8, col 0")
    print("   Meta   : esquina superior-izquierda  (F) = fila 0, col 0")
    print("   Vidas  : 3 iniciales  |  inviable si vidas < 0")
    print("=" * 64)

    imprimir_laberinto("LABERINTO ORIGINAL:")

    visitado = [[False] * COLS for _ in range(FILAS)]
    fi, ci = INICIO
    visitado[fi][ci] = True
    camino = []

    print("─" * 64)
    print("RECORRIDO PASO A PASO (backtracking):")
    print("─" * 64)

    encontrado = backtracking(fi, ci, VIDAS_INICIALES, camino, visitado)

    print("\n" + "=" * 64)
    if encontrado:
        print("   ✅  ¡SALIDA ENCONTRADA!")
        print("=" * 64)
        print(f"\n   Total de pasos: {len(camino)}\n")
        vv = VIDAS_INICIALES
        for paso, (r, c) in enumerate(camino):
            celda = laberinto[r][c]
            vv += costo(celda)
            marca = "⚠" if vv == 0 else " "
            print(f"  {marca} Paso {paso+1:2d}: fila={r}  col={c}"
                  f"  celda={str(celda):>3}  vidas restantes = {vv}")

        cs = set(camino)
        imprimir_laberinto("LABERINTO — camino marcado con  *:", cs)

        print("MATRIZ DE SALIDA (camino = *):\n")
        for i, fila in enumerate(laberinto):
            linea = ""
            for j, celda in enumerate(fila):
                if (i, j) in cs:
                    linea += f"{'*':>4}"
                else:
                    linea += f"{str(celda):>4}"
            print(linea)
    else:
        print("   ❌  NO SE ENCONTRÓ SALIDA VIABLE")
        print("   El ratón no puede llegar a la meta sin perder todas sus vidas.")
    print("\n" + "=" * 64)


if __name__ == "__main__":
    main()