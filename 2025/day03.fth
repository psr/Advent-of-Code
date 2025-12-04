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
  cell+ dup c@ swap             ( next-addr u node-addr+1cell )
  char+ swap                    ( next-addr c-addr u )
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
  negate allot here <> throw ; \ Untested, might be wrong.

\ initialise with nulls
: populate-buffer ( c_addr u -- )
  chars over + swap ( end_address start_address )
  do 0 i c! 1 chars +loop
;

: 3dup  ( a b c -- a b c a b c )
  DUP 2OVER ROT ;

: copy-digits-from-window      ( buffer_len data_addr buffer_addr -- )
  2 pick 0 do                   ( buffer_len data_addr buffer_addr )
    over i chars + c@           ( b_len d_addr b_addr d[i] )
    over i chars + c@           ( b_len d_addr b_addr d[i] b[i] )
    > if			( b_len d_addr b_addr )
      rot rot                   ( b_addr b_len d_addr )
      i chars +                 ( b_addr b_len d_addr+i )
      rot rot i /string         ( d_addr+i b_addr+i b_len-i  )
      cmove                     (  )
      unloop exit
    then                        ( b_len d_addr b_addr )
  loop
  drop drop drop
;

\ Slide a window over the data, copying best digits found into the buffer
: find-best-digits    ( data_addr data_len buffer_addr buffer_len -- )
  2swap rot           ( b_addr d_addr d_len b_len )
  tuck - 1+ >r        ( b_addr d_addr b_len ) ( r: trip_count)
  rot rot             ( b_len d_addr b_addr )
  r> 0 do	      ( b_len d_addr b_addr ) ( r: )
    3dup copy-digits-from-window ( b_len d_addr b_addr )
    swap char+ swap              \ Advance data pointer.
  loop
  drop drop drop                (  )
;


: read-number ( c_addr u - ud )
  0 0 2swap >number 2drop ;


: find-best-joltage ( data_addr data_len buffer_addr buffer_len -- ud )
  2dup populate-buffer          ( d_addr d_len b_addr b_len )
  2swap 2over find-best-digits  ( b_addr b_len )
  read-number                   ( ud )
;


: solve                     ( head_addr digits -- ud )
  0 0 2swap                 ( acc_d head_addr digits)
  allocate-buffer rot       ( acc_d buffer_addr buffer_len head_addr )
  begin dup while           ( acc_d buffer_addr buffer_len head_addr )
       read-list-header  ( acc_d b_addr b_len next_addr d_addr d_len )
       rot >r     ( acc_d b_addr b_len d_addr d_len ) ( R: next_addr )
       2over find-best-joltage  ( acc_d b_addr b_len joltage_d )
       2rot d+ 2swap            ( acc_d b_addr b_len next_addr )
       r>                       ( next_addr ) ( R: )
       repeat                   ( acc_d b_addr b_len 0 )
  drop release-buffer           ( acc_d )
;

: part-1 2 solve ;
: part-2 12 solve ;

read-input dup
." Part 1: " part-1 d. cr
." Part 2: " part-2 d. cr
bye
