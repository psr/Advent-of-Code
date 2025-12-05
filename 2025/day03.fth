128 constant line-buffer-length
create line-buffer line-buffer-length chars allot


\ Store lines from standard input in a linked list
\ Each node is a next pointer (or zero), a length, then character data
: read-input                    ( -- head-addr )
  0                             ( next-addr )
  begin
    line-buffer dup line-buffer-length 2 - stdin read-line throw over and
  while                         ( next-addr c-addr u )
    rot align here >r ,         ( c-addr u ) ( R: new-next-addr )
    dup c,                      ( c-addr u )
    here over chars allot       ( src-addr u dest-addr )
    swap cmove
    r>                          ( new-next-addr )
  repeat
  2drop
;

: read-list-header              ( node-addr -- next-addr c-addr u )
  dup @ swap                    ( next-addr node-addr )
  cell+ count
;

: print-input ( head-addr -- )
  begin
    dup
  while
    read-list-header type cr
  repeat
  drop
;

: allocate-buffer                       ( u1 -- c-addr u1 )
  here swap dup chars allot ;

: release-buffer                ( c-addr u -- )
  negate allot here <> throw ;


\ Find the point (if any), where a digit in the window is greater than
\ the corresponding digit in the buffer. The data addr returned is a
\ pointer to the higher digit, and the index of the buffer where it
\ must be copied is returned. -1 represents all digits are smaller.
: compare-window		( data_addr1 buffer_addr buffer_len -- data_addr2 u | -1 )
  0 do				( data_addr buffer_addr )
    over c@ over c@		( d_addr b_addr data[i] buffer[i] )
    > if drop i unloop exit then
    char+ swap char+ swap loop	  \ Increment pointers
  2drop -1 ;


: copy-digits-from-window      ( data_addr buffer_addr buffer_len -- )
  2dup 2>r compare-window
  \ If we found a higher digit, restore the original buffer adjust it
  \ and copy the data, otherwise drop everything.
  dup 0< if drop 2r> 2drop else 2r> rot /string cmove then ;

\ Slide a window over the data, copying best digits found into the buffer
: find-best-digits    ( data_addr data_len buffer_addr buffer_len -- )
  dup >r
  2swap r> - 1+	\ Adjust data length so window doesn't go off the end.
  chars bounds do	( buffer_addr buffer_len )
    2dup i -rot copy-digits-from-window
    [ 1 chars ] literal +loop
  2drop ;


: read-number ( c_addr u - ud )
  0 0 2swap >number 2drop ;

: find-best-joltage ( data_addr data_len buffer_addr buffer_len -- ud )
  2dup erase	    ( d_addr d_len b_addr b_len )
  2swap 2over find-best-digits  ( b_addr b_len )
  read-number                   ( ud )
;


: solve                     ( head_addr digits -- ud )
  0 0 2swap                 ( acc_d head_addr digits)
  allocate-buffer rot       ( acc_d buffer_addr buffer_len head_addr )
  begin dup while           ( acc_d buffer_addr buffer_len head_addr )
    read-list-header	 ( acc_d b_addr b_len next_addr d_addr d_len )
    rot >r	  ( acc_d b_addr b_len d_addr d_len ) ( R: next_addr )
    2over find-best-joltage	( acc_d b_addr b_len joltage_d )
    2rot d+ 2swap		( acc_d b_addr b_len next_addr )
    r>				( next_addr ) ( R: )
  repeat			( acc_d b_addr b_len 0 )
  drop release-buffer           ( acc_d )
;


: part-1 2 solve ;
: part-2 12 solve ;


read-input dup
." Part 1: " part-1 d. cr
." Part 2: " part-2 d. cr
bye
