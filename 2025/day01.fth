128 constant line-buffer-length
create line-buffer line-buffer-length chars allot

\ Convert L to -1 and anything else (R) to 1
: convert-direction ( char -- n )
  [char] L = 1 or ;  \ I don't care that an if might be better. I like it.

\ Parses the number starting at addr with length u
\ Returns a single cell number
: parse-number ( addr u - u )
  0 0 2swap >number 2drop drop ;

: parse-line ( addr u - n )
  over c@ convert-direction >r
  1 /string
  parse-number
  r> * ;

: parse-input ( -- addr u )
  align here \ beginning of array
  0 \ count of cells in array
  begin
    \ Read a line from standard input into line-buffer, throwing on error.
    \ Will stop looping if the line is empty or the read fails.
    \ Maximum amount is -2 for line ending characters.
    line-buffer line-buffer-length 2 - stdin read-line throw over and
  while ( u )  \ count of bytes read.
    line-buffer swap parse-line ,
    1+ \ Increment array length.
  repeat
  drop \ Count of bytes read
;

: print-numbers ( addr1 u1 -- addr1 u1)
  2dup 0 do dup @ . cell+ cr loop drop ;

: part-1 ( addr1 u1 -- u2 )
  0  \ count of zeros
  50 \ initial dial position
  2swap cells over + swap \ Array to loop params ( zeros pos end start )
  do ( zeros pos )
    I @ + 100 mod ( zeros new-pos )
    tuck 0= - swap ( new-zeros new-pos )
    1 cells +loop
  drop \ pos
;

parse-input 2dup
." Part 1: " part-1 . cr
bye
