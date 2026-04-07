(function () {
    var CHART_IDS = ['barra_cnn', 'pie_cnn', 'barra_dnn', 'pie_dnn'];
    var CHART_LABELS = [
        'CNN — Gráfico de barras',
        'CNN — Gráfico circular',
        'DNN — Gráfico de barras',
        'DNN — Gráfico circular'
    ];

    function getJsPDFConstructor() {
        if (window.jspdf && window.jspdf.jsPDF) {
            return window.jspdf.jsPDF;
        }
        if (typeof window.jsPDF === 'function') {
            return window.jsPDF;
        }
        return null;
    }

    function plotToPng(id) {
        var el = document.getElementById(id);
        if (!el) {
            return Promise.reject(new Error('No se encontró la gráfica: ' + id));
        }
        return Plotly.toImage(el, { format: 'png', width: 900, height: 520 });
    }

    function exportDashboardPdf() {
        var JsPDF = getJsPDFConstructor();
        if (!JsPDF) {
            return Promise.reject(new Error('jsPDF no está disponible'));
        }
        if (typeof Plotly === 'undefined' || typeof Plotly.toImage !== 'function') {
            return Promise.reject(new Error('Plotly no está disponible'));
        }

        var doc = new JsPDF({ unit: 'mm', format: 'a4', orientation: 'portrait' });
        var pageW = doc.internal.pageSize.getWidth();
        var pageH = doc.internal.pageSize.getHeight();
        var margin = 12;
        var contentW = pageW - 2 * margin;
        var imgH = contentW * (520 / 900);
        var y = margin;

        doc.setFontSize(15);
        doc.setTextColor(30);
        doc.text('Dashboard — Gráficas', margin, y);
        y += 9;

        var chain = Promise.resolve();

        CHART_IDS.forEach(function (id, i) {
            chain = chain.then(function () {
                return plotToPng(id);
            }).then(function (dataUrl) {
                var captionH = 6;
                if (y + captionH + imgH > pageH - margin) {
                    doc.addPage();
                    y = margin;
                }
                doc.setFontSize(10);
                doc.setTextColor(55);
                doc.text(CHART_LABELS[i], margin, y);
                y += captionH;
                doc.addImage(dataUrl, 'PNG', margin, y, contentW, imgH);
                y += imgH + 8;
            });
        });

        return chain.then(function () {
            var stamp = new Date().toISOString().slice(0, 10);
            doc.save('dashboard_graficas_' + stamp + '.pdf');
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var btn = document.getElementById('btnDescargarPdf');
        if (!btn) {
            return;
        }

        btn.addEventListener('click', function () {
            var original = btn.textContent;
            btn.disabled = true;
            btn.setAttribute('aria-busy', 'true');
            btn.textContent = 'Generando PDF…';

            exportDashboardPdf().catch(function (err) {
                console.error(err);
                alert('No se pudo generar el PDF. ' + (err && err.message ? err.message : ''));
            }).finally(function () {
                btn.disabled = false;
                btn.removeAttribute('aria-busy');
                btn.textContent = original;
            });
        });
    });
})();
