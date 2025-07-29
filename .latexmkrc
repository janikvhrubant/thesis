$cleanup_includes_cus = 1;
END {
    system("find . -type f \\( -name '*.aux' -o -name '*.log' -o -name '*.toc' -o -name '*.bbl' -o -name '*.blg' -o -name '*.out' -o -name '*.fdb_latexmk' -o -name '*.fls' -o -name '*.synctex.gz' -o -name '*.run.xml' \\) -delete");
}
