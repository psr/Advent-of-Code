128 constant line-buffer-length
create line-buffer line-buffer-length chars allot

\ Convert L to -1 and anything else (R) to 1
: convert-direction ( c -- n )
  [char] L = 1 or ;  \ I don't care that an if might be better. I like it.

\ Parses the number starting at addr with length u
\ Returns a single cell number
: parse-number ( caddr u - u )
  0 0 2swap >number 2drop drop ;

: parse-line ( caddr u - n )
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

\ Takes the initial dial position, and a movement, returns the
\ zero-crossings and the dial position
: count-zero-crossings		( u n -- u u )
  \ If we start on zero, and do a negative movement /mod will always say
  \ we've done one more rotation than we have.
  \ Otherwise negative movement is fine.
  \ We also want to store whether the movement was negative for later.
  2dup 0< dup >r swap 0= and	( pos move correction ) ( R: move<0 )
  rot rot			( correction pos move )
  + 100 /mod abs		( correction new-pos zeros )
  \ If we end on a zero as a result of a negative rotation, we've
  \ we must add it as a further correction.
  over 0= r> and -		( correction new-pos zeros ) ( R: )
  rot +				( new-pos zeros )
;

: part-2 ( addr1 u1 -- u2 )
  0  \ count of zeros
  50 \ initial dial position
  2swap cells over + swap \ Array to loop params ( zeros pos end start )
  do ( zeros pos )
    I @ count-zero-crossings ( zeros new-pos additional-zeros )
    rot + swap ( new-zeros new-pos )
    1 cells +loop
  drop \ pos
;


parse-input 2dup
." Part 1: " part-1 . cr
." Part 2: " part-2 . cr
bye
