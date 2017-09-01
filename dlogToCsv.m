arg_list = argv ();
filename_in = arg_list{1};
period = str2double(arg_list{2});
filename_out = arg_list{3};

id = fopen(filename_in, "r");
[number_values, r] = fread(id,1,"uint64", 0, "ieee-be");

[v, count] = fread(id,Inf,"float32", 0, "ieee-be");

v2 = [v v];
for i = 1:count
    v2(i,1) = (i)*period;
endfor

csvwrite(filename_out, v2);
