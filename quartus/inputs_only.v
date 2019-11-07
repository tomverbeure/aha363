module top(
	input clk,
	input wire [400:0] all_inputs
	//output wire [7:0] some_outputs
   //output wire [2:0] pgm
);

	reg result /* synthesis noprune */;
	
	//assign some_outputs = 8'haa;

	always @(posedge clk) 
		result = ^all_inputs;

    reg reset;
	 initial
		reset <= 1'b1;
    always @(posedge clk)
        reset <= 1'b0;
		
/*
	remote_update   remote_update_inst (
    .clock ( clk ),
    .reset ( reset ),
    .param ( 0),
    .reconfig ( 1'b0 ),
    .busy ( ),

    .read_param (1'b0),
    .data_out ( ),

    .pgmout ( pgm )
    );
*/
		

endmodule
