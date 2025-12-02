128 constant line-buffer-length
create line-buffer line-buffer-length chars allot

: parse-input ( -- addr u )
  align
  here ( beginning of array )
  0 ( count of cells )
  begin line-buffer line-buffer-length 2 - stdin read-line drop over and
  while
    line-buffer c@ [char] L = 1 or swap
    1- line-buffer char+ swap 0 0 2swap  >number 2drop drop * ,
    1+
  repeat
  drop
;


: print-numbers ( addr1 u1 -- addr1 u1)
  2dup 0 do dup @ . cell+ cr loop drop ;

: part-1 ( addr1 u1 -- u3 )
  0 50 ( ptr, len, total zeros, starting position )
  2swap 0 do 
    dup @ swap cell+ swap ( zeros, position, ptr, current )
    rot + 100 mod ( zeros, ptr, pos )
    dup 0= negate 3 roll + ( ptr, pos, zeros )
    rot rot swap ( zeros, pos, ptr )
  loop
  2drop
;

parse-input 2dup 
." Part 1: " part-1 . cr
\ ." Part 2: " part-2 . cr
bye
