%subplot(2, 1, 1)

o = csvread("ecdf_original.csv")(:, [2, 3]);
d = csvread("ecdf_dropped.csv")(:, [2, 3]);
plot(o(:, 1), o(:, 2), 'rx', 'markersize', 2, d(:, 1), d(:, 2), 'bo', 'markersize', 2)
legend("Original", "Modified")

%subplot(2, 2, 3)
%o = csvread("original.csv");
%d = csvread("dropped.csv");
%[on ov] = hist(o, 100);
%[dn dv] = hist(d, 100);
%plot(ov, on, 'r', dv, dn, 'b')

%subplot(2, 2, 4)
%[on ov] = hist(o, 50);
%[dn dv] = hist(d, 50);
%plot(ov, on, 'r', dv, dn, 'b')

