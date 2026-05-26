# MATLAB Publication-Quality Figure Style

## Figure Setup Template

`matlab
% Publication figure template
figure('Position', [100 100 800 600]);  % 4:3 aspect
set(gcf, 'Color', 'w');

% Plot data
plot(x, y, 'LineWidth', 1.5);
hold on;
% ... additional plots ...

% Labels
xlabel('x/D', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('C_p', 'Interpreter', 'latex', 'FontSize', 14);
title('Pressure Coefficient Distribution', 'FontSize', 14);

% Axis styling
set(gca, 'FontSize', 12, 'LineWidth', 1);
set(gca, 'TickLabelInterpreter', 'latex');
grid on;
box on;

% Legend
legend('Exp.', 'CFD', 'Location', 'best', 'FontSize', 12);
legend boxoff;

% Export
exportgraphics(gcf, 'figure.eps', 'Resolution', 600);
exportgraphics(gcf, 'figure.png', 'Resolution', 300);
`

## Key Settings

| Property | Journal Paper | Conference / Report |
|----------|--------------|---------------------|
| Font size (axes) | 12-14 pt | 11-12 pt |
| Font size (labels) | 14-16 pt | 12-14 pt |
| Line width | 1.5-2 pt | 1-1.5 pt |
| Marker size | 6-8 | 4-6 |
| Resolution | 600 DPI (EPS/PDF) | 300 DPI |
| Figure width | Column: ~8 cm, Full: ~16 cm | Slide: ~12 cm |
| Color | Grayscale or color-blind safe | Color OK |

## Color Maps for CFD

`matlab
% Jet -- avoid (perceptually nonlinear). Use instead:
colormap(parula);     % MATLAB default, perceptually uniform
colormap(viridis);    % Python-style, colorblind-safe
colormap(jet);        % ONLY if journal requires it

% Custom diverging (for Cp, etc.)
n = 256;
blue = [0 0 0.5]; white = [1 1 1]; red = [0.5 0 0];
cmap = [linspace(blue(1),white(1),n/2)' linspace(blue(2),white(2),n/2)' linspace(blue(3),white(3),n/2)';
        linspace(white(1),red(1),n/2)' linspace(white(2),red(2),n/2)' linspace(white(3),red(3),n/2)'];
colormap(cmap);
`

## Common CFD Plots

### Velocity profiles
`matlab
plot(U_mean, y, 'b-o', 'LineWidth', 1.5, 'MarkerSize', 6);
xlabel('U/U_b', 'Interpreter', 'latex');
ylabel('y/H', 'Interpreter', 'latex');
`

### Cp distribution
`matlab
plot(x/c, -Cp, 'r-', 'LineWidth', 1.5);  % Note: NEGATIVE Cp for airfoils
set(gca, 'YDir', 'reverse');             % Invert Y axis (aerospace convention)
`

### Contour plots
`matlab
contourf(X, Y, Z, 50, 'LineStyle', 'none');
colorbar;
axis equal;
`

## Export Formats

| Format | Use For | Command |
|--------|---------|---------|
| EPS | LaTeX papers (vector) | exportgraphics(gcf, 'fig.eps', 'Resolution', 600) |
| PDF | General vector | exportgraphics(gcf, 'fig.pdf') |
| PNG | Word/PowerPoint | exportgraphics(gcf, 'fig.png', 'Resolution', 300) |
| TIFF | Journals requiring raster | exportgraphics(gcf, 'fig.tiff', 'Resolution', 600) |

## Load OpenFOAM Data into MATLAB

`matlab
% Read sampled data from postProcess
data = readtable('postProcessing/sample/0/line_U.xy', ...
    'FileType', 'text', 'CommentStyle', '#');
x = data.Var1;  % position
Ux = data.Var2;
Uy = data.Var3;
Uz = data.Var4;
`
