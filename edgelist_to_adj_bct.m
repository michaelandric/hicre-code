% read edgelist and operate
% make adjacency matrix
% do bct functions

% have to unzip edgelists
gunzip('CB.dens_0.1.edgelist.gz');
gunzip('SCB.dens_0.1.edgelist.gz');

% read in edgelists
cb = dlmread('CB.dens_0.1.edgelist');
scb = dlmread('SCB.dens_0.1.edgelist')

% indices cannot start at 0
cb1 = cb+1;
scb1 = scb + 1;

% because there are 1087 edges
n_edges = 1087;
% weight vector. this is binary undirected 
w = repmat(1, n_edges, 1)

% THIS GIVES ONLY UPPER TRIANGLE
m = sparse(cb1(:, 1), cb1(:, 2), w, 148, 148)
mm = full(m);
% FILL OUT THE TRIUL GET COMPLETE ADJ MATRIX
A = mm + triu(mm, 1)';

deg = degrees_und(A);
cc = clustering_coef_bu(A);
