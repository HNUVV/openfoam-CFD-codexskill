%% OpenFOAM Post-Processing Template for Publication Figures
% Load OpenFOAM sampled data and create publication-quality plots

clear; close all; clc;

%% ===== USER SETTINGS =====
case_dir = 'REPLACE_CASE_PATH';
sample_dir = fullfile(case_dir, 'postProcessing', 'sample');

% Figure export path
export_dir = fullfile(case_dir, 'figures');
if ~exist(export_dir, 'dir')
    mkdir(export_dir);
end

%% ===== PLOT SETTINGS (Publication Quality) =====
set(0, 'DefaultAxesFontSize', 12);
set(0, 'DefaultAxesLineWidth', 1);
set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesTickLabelInterpreter', 'latex');
marker_size = 6;

%% ===== 1. Velocity Profile =====
% Load sampled data (XY format from OpenFOAM sample utility)
% data = readtable(fullfile(sample_dir, '0', 'line_U.xy'), 'FileType', 'text', 'CommentStyle', '#');

% Example: parabolic profile
y = linspace(0, 1, 50);
U = 4 * y .* (1 - y);  % replace with actual data

figure('Position', [100 100 500 400], 'Color', 'w');
plot(U, y, 'b-o', 'LineWidth', 1.5, 'MarkerSize', marker_size);
xlabel('$$U/U_b$$', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('$$y/H$$', 'Interpreter', 'latex', 'FontSize', 14);
grid on; box on;
exportgraphics(gcf, fullfile(export_dir, 'velocity_profile.eps'), 'Resolution', 600);
exportgraphics(gcf, fullfile(export_dir, 'velocity_profile.png'), 'Resolution', 300);
disp('Saved: velocity_profile');

%% ===== 2. Cp Distribution =====
x_c = linspace(0, 1, 100);
Cp = 1 - 4 * x_c.^2;  % replace with actual data

figure('Position', [100 100 500 400], 'Color', 'w');
plot(x_c, -Cp, 'r-', 'LineWidth', 1.5);
xlabel('$$x/c$$', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('$$-C_p$$', 'Interpreter', 'latex', 'FontSize', 14);
set(gca, 'YDir', 'reverse');
grid on; box on;
exportgraphics(gcf, fullfile(export_dir, 'cp_distribution.eps'), 'Resolution', 600);
disp('Saved: cp_distribution');

%% ===== 3. Contour Plot =====
[X, Y] = meshgrid(linspace(0, 1, 50), linspace(0, 0.5, 30));
Z = sin(pi * X) .* cos(2 * pi * Y);  % replace with actual data

figure('Position', [100 100 600 400], 'Color', 'w');
contourf(X, Y, Z, 30, 'LineStyle', 'none');
colormap(parula);
colorbar;
xlabel('$$x$$', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('$$y$$', 'Interpreter', 'latex', 'FontSize', 14);
axis equal tight;
box on;
exportgraphics(gcf, fullfile(export_dir, 'contour.eps'), 'Resolution', 600);
disp('Saved: contour');

%% ===== 4. Comparison Plot (CFD vs Experiment) =====
x_exp = linspace(0, 1, 10);
y_exp = 1 - 2 * x_exp + 0.1 * randn(1, 10);  % replace
x_cfd = linspace(0, 1, 50);
y_cfd = 1 - 2 * x_cfd;  % replace

figure('Position', [100 100 500 400], 'Color', 'w');
h1 = plot(x_exp, y_exp, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k');
hold on;
h2 = plot(x_cfd, y_cfd, 'r-', 'LineWidth', 1.5);
xlabel('$$x$$', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('$$C_f$$', 'Interpreter', 'latex', 'FontSize', 14);
legend([h1, h2], {'Experiment', 'CFD'}, 'Location', 'best', 'FontSize', 12);
legend boxoff;
grid on; box on;
exportgraphics(gcf, fullfile(export_dir, 'comparison.eps'), 'Resolution', 600);
disp('Saved: comparison');

%% ===== 5. FFT / Spectral Analysis =====
% For unsteady flows: time series to frequency spectrum
% data = load(fullfile(sample_dir, 'probe_data.txt'));
% t = data(:,1); signal = data(:,2);
% Fs = 1 / mean(diff(t));
% N = length(signal);
% f = Fs * (0:(N/2)) / N;
% Y = fft(signal - mean(signal));
% P = abs(Y(1:N/2+1)).^2 / N;

% figure('Position', [100 100 500 400], 'Color', 'w');
% semilogy(f, P, 'b-', 'LineWidth', 1.5);
% xlabel('$$f$$ (Hz)', 'Interpreter', 'latex', 'FontSize', 14);
% ylabel('$$P(f)$$', 'Interpreter', 'latex', 'FontSize', 14);
% grid on; box on;

disp('All figures saved to:');
disp(export_dir);
