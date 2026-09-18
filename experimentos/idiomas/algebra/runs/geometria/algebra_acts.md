# Algebra de direcciones: el paralelogramo en activaciones

Delta del ultimo token del prompt contra la pregunta sin parche, n = 50. La capa 0 no significa nada con goal_all (el ultimo token no se toca).

- `v* → real`: activaciones que produce v* (el vector compuesto, metido en el embedding) contra las de v_real.
- `act → real`: Δh(s) + Δh(o) − Δh(d), el algebra hecha directamente en activaciones, contra Δh(real).
- `s → real`, `suma → real`: contexto, lo que ya se parecian sin algebra.

## coseno de las medias

| paralelogramo | serie | L4 | L8 | L12 | L16 | L20 | L24 | L28 |
|---|---|---|---|---|---|---|---|---|
| fr=fr_up+es-es_up | v* → real | 0.490 | 0.714 | 0.791 | 0.601 | 0.581 | 0.633 | 0.641 |
| fr=fr_up+es-es_up | act → real | 0.384 | 0.571 | 0.734 | 0.792 | 0.863 | 0.900 | 0.867 |
| fr=fr_up+es-es_up | s → real | 0.483 | 0.636 | 0.777 | 0.775 | 0.825 | 0.871 | 0.663 |
| fr=fr_up+es-es_up | suma → real | 0.622 | 0.788 | 0.872 | 0.861 | 0.882 | 0.869 | 0.761 |
| fr_up=fr+es_up-es | v* → real | 0.493 | 0.654 | 0.727 | 0.677 | 0.670 | 0.717 | 0.633 |
| fr_up=fr+es_up-es | act → real | 0.444 | 0.610 | 0.771 | 0.851 | 0.905 | 0.931 | 0.925 |
| fr_up=fr+es_up-es | s → real | 0.483 | 0.636 | 0.777 | 0.775 | 0.825 | 0.871 | 0.663 |
| fr_up=fr+es_up-es | suma → real | 0.525 | 0.702 | 0.836 | 0.857 | 0.895 | 0.901 | 0.861 |
| es=es_up+fr-fr_up | v* → real | 0.447 | 0.773 | 0.831 | 0.751 | 0.796 | 0.830 | 0.853 |
| es=es_up+fr-fr_up | act → real | 0.422 | 0.652 | 0.736 | 0.803 | 0.881 | 0.908 | 0.877 |
| es=es_up+fr-fr_up | s → real | 0.495 | 0.721 | 0.831 | 0.838 | 0.882 | 0.879 | 0.690 |
| es=es_up+fr-fr_up | suma → real | 0.620 | 0.807 | 0.884 | 0.883 | 0.904 | 0.862 | 0.775 |
| es_up=es+fr_up-fr | v* → real | 0.439 | 0.714 | 0.825 | 0.801 | 0.828 | 0.799 | 0.619 |
| es_up=es+fr_up-fr | act → real | 0.365 | 0.570 | 0.776 | 0.820 | 0.890 | 0.913 | 0.923 |
| es_up=es+fr_up-fr | s → real | 0.495 | 0.721 | 0.831 | 0.838 | 0.882 | 0.879 | 0.690 |
| es_up=es+fr_up-fr | suma → real | 0.540 | 0.777 | 0.882 | 0.907 | 0.933 | 0.910 | 0.881 |
| fr=fr_up+de-de_up | v* → real | 0.512 | 0.687 | 0.797 | 0.704 | 0.672 | 0.615 | 0.556 |
| fr=fr_up+de-de_up | act → real | 0.481 | 0.612 | 0.743 | 0.697 | 0.755 | 0.806 | 0.794 |
| fr=fr_up+de-de_up | s → real | 0.483 | 0.636 | 0.777 | 0.775 | 0.825 | 0.871 | 0.663 |
| fr=fr_up+de-de_up | suma → real | 0.601 | 0.802 | 0.878 | 0.861 | 0.864 | 0.831 | 0.749 |
| fr_up=fr+de_up-de | v* → real | 0.553 | 0.672 | 0.750 | 0.752 | 0.770 | 0.783 | 0.708 |
| fr_up=fr+de_up-de | act → real | 0.407 | 0.603 | 0.732 | 0.802 | 0.857 | 0.872 | 0.877 |
| fr_up=fr+de_up-de | s → real | 0.483 | 0.636 | 0.777 | 0.775 | 0.825 | 0.871 | 0.663 |
| fr_up=fr+de_up-de | suma → real | 0.556 | 0.676 | 0.797 | 0.824 | 0.881 | 0.884 | 0.841 |
| de=de_up+fr-fr_up | v* → real | 0.393 | 0.716 | 0.760 | 0.654 | 0.689 | 0.702 | 0.730 |
| de=de_up+fr-fr_up | act → real | 0.307 | 0.664 | 0.674 | 0.742 | 0.790 | 0.814 | 0.784 |
| de=de_up+fr-fr_up | s → real | 0.427 | 0.741 | 0.808 | 0.778 | 0.795 | 0.826 | 0.616 |
| de=de_up+fr-fr_up | suma → real | 0.565 | 0.825 | 0.880 | 0.826 | 0.820 | 0.788 | 0.707 |
| de_up=de+fr_up-fr | v* → real | 0.524 | 0.764 | 0.835 | 0.761 | 0.767 | 0.811 | 0.738 |
| de_up=de+fr_up-fr | act → real | 0.386 | 0.547 | 0.698 | 0.725 | 0.803 | 0.834 | 0.861 |
| de_up=de+fr_up-fr | s → real | 0.427 | 0.741 | 0.808 | 0.778 | 0.795 | 0.826 | 0.616 |
| de_up=de+fr_up-fr | suma → real | 0.533 | 0.767 | 0.827 | 0.864 | 0.892 | 0.873 | 0.829 |
| es=es_up+de-de_up | v* → real | 0.508 | 0.785 | 0.856 | 0.800 | 0.746 | 0.653 | 0.594 |
| es=es_up+de-de_up | act → real | 0.517 | 0.650 | 0.774 | 0.728 | 0.812 | 0.833 | 0.812 |
| es=es_up+de-de_up | s → real | 0.495 | 0.721 | 0.831 | 0.838 | 0.882 | 0.879 | 0.690 |
| es=es_up+de-de_up | suma → real | 0.635 | 0.831 | 0.905 | 0.889 | 0.895 | 0.838 | 0.763 |
| es_up=es+de_up-de | v* → real | 0.404 | 0.676 | 0.774 | 0.749 | 0.782 | 0.758 | 0.584 |
| es_up=es+de_up-de | act → real | 0.297 | 0.616 | 0.763 | 0.830 | 0.892 | 0.885 | 0.883 |
| es_up=es+de_up-de | s → real | 0.495 | 0.721 | 0.831 | 0.838 | 0.882 | 0.879 | 0.690 |
| es_up=es+de_up-de | suma → real | 0.549 | 0.762 | 0.854 | 0.883 | 0.920 | 0.891 | 0.850 |
| de=de_up+es-es_up | v* → real | 0.464 | 0.724 | 0.771 | 0.643 | 0.659 | 0.673 | 0.683 |
| de=de_up+es-es_up | act → real | 0.269 | 0.627 | 0.712 | 0.760 | 0.823 | 0.836 | 0.789 |
| de=de_up+es-es_up | s → real | 0.427 | 0.741 | 0.808 | 0.778 | 0.795 | 0.826 | 0.616 |
| de=de_up+es-es_up | suma → real | 0.621 | 0.831 | 0.892 | 0.828 | 0.824 | 0.794 | 0.704 |
| de_up=de+es_up-es | v* → real | 0.513 | 0.751 | 0.788 | 0.638 | 0.636 | 0.641 | 0.660 |
| de_up=de+es_up-es | act → real | 0.388 | 0.601 | 0.725 | 0.799 | 0.866 | 0.875 | 0.870 |
| de_up=de+es_up-es | s → real | 0.427 | 0.741 | 0.808 | 0.778 | 0.795 | 0.826 | 0.616 |
| de_up=de+es_up-es | suma → real | 0.492 | 0.784 | 0.846 | 0.879 | 0.899 | 0.880 | 0.822 |

## media de cosenos prompt a prompt

| paralelogramo | serie | L4 | L8 | L12 | L16 | L20 | L24 | L28 |
|---|---|---|---|---|---|---|---|---|
| fr=fr_up+es-es_up | v* → real | 0.477 | 0.661 | 0.708 | 0.558 | 0.551 | 0.560 | 0.550 |
| fr=fr_up+es-es_up | act → real | 0.364 | 0.507 | 0.622 | 0.660 | 0.738 | 0.774 | 0.748 |
| fr_up=fr+es_up-es | v* → real | 0.484 | 0.610 | 0.664 | 0.658 | 0.667 | 0.683 | 0.596 |
| fr_up=fr+es_up-es | act → real | 0.421 | 0.549 | 0.666 | 0.735 | 0.805 | 0.833 | 0.836 |
| es=es_up+fr-fr_up | v* → real | 0.440 | 0.731 | 0.755 | 0.648 | 0.697 | 0.712 | 0.732 |
| es=es_up+fr-fr_up | act → real | 0.405 | 0.593 | 0.631 | 0.656 | 0.757 | 0.790 | 0.761 |
| es_up=es+fr_up-fr | v* → real | 0.425 | 0.666 | 0.756 | 0.719 | 0.749 | 0.687 | 0.555 |
| es_up=es+fr_up-fr | act → real | 0.344 | 0.508 | 0.673 | 0.703 | 0.785 | 0.806 | 0.829 |
| fr=fr_up+de-de_up | v* → real | 0.497 | 0.634 | 0.704 | 0.633 | 0.602 | 0.536 | 0.493 |
| fr=fr_up+de-de_up | act → real | 0.452 | 0.547 | 0.633 | 0.583 | 0.654 | 0.693 | 0.680 |
| fr_up=fr+de_up-de | v* → real | 0.546 | 0.632 | 0.685 | 0.704 | 0.734 | 0.727 | 0.657 |
| fr_up=fr+de_up-de | act → real | 0.389 | 0.537 | 0.622 | 0.707 | 0.780 | 0.785 | 0.788 |
| de=de_up+fr-fr_up | v* → real | 0.381 | 0.680 | 0.692 | 0.597 | 0.637 | 0.636 | 0.650 |
| de=de_up+fr-fr_up | act → real | 0.296 | 0.600 | 0.569 | 0.626 | 0.696 | 0.708 | 0.675 |
| de_up=de+fr_up-fr | v* → real | 0.513 | 0.702 | 0.724 | 0.650 | 0.655 | 0.638 | 0.582 |
| de_up=de+fr_up-fr | act → real | 0.368 | 0.487 | 0.584 | 0.619 | 0.712 | 0.734 | 0.758 |
| es=es_up+de-de_up | v* → real | 0.487 | 0.734 | 0.759 | 0.657 | 0.613 | 0.523 | 0.508 |
| es=es_up+de-de_up | act → real | 0.487 | 0.597 | 0.671 | 0.582 | 0.682 | 0.711 | 0.690 |
| es_up=es+de_up-de | v* → real | 0.400 | 0.646 | 0.718 | 0.694 | 0.736 | 0.697 | 0.572 |
| es_up=es+de_up-de | act → real | 0.288 | 0.558 | 0.658 | 0.714 | 0.799 | 0.792 | 0.792 |
| de=de_up+es-es_up | v* → real | 0.443 | 0.683 | 0.697 | 0.579 | 0.607 | 0.597 | 0.602 |
| de=de_up+es-es_up | act → real | 0.260 | 0.570 | 0.603 | 0.629 | 0.707 | 0.717 | 0.673 |
| de_up=de+es_up-es | v* → real | 0.501 | 0.680 | 0.667 | 0.564 | 0.567 | 0.532 | 0.536 |
| de_up=de+es_up-es | act → real | 0.370 | 0.546 | 0.609 | 0.661 | 0.754 | 0.767 | 0.768 |

