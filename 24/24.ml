open Containers

let lines = IO.with_in "in.txt" IO.read_lines_l

type value =
  | Digit of int
  | Lit of int
  | Add of value * value
  | Mul of value * value
  | Mod of value * value
  | Div of value * value
  | Eql of value * value
  | Neq of value * value

type state =
  { x: value
  ; y: value
  ; z: value
  ; w: value
  }

type frame =
  { state: state
  ; digit: int
  }

let get state c =
  match c with
  | "x" -> state.x
  | "y" -> state.y
  | "z" -> state.z
  | "w" -> state.w
  | _ -> Lit (Int.of_string_exn c)

let set state c v =
  match c with
  | "x" -> {state with x=v}
  | "y" -> {state with y=v}
  | "z" -> {state with z=v}
  | "w" -> {state with w=v}
  | _ -> failwith "invalid set key"

let rec operate op a b =
  ignore a; ignore b;
  match op with
  | "add" ->
      (match a, b with
      | (Lit 0, x) | (x, Lit 0) -> x
      | (Lit m, Lit n) -> Lit (m+n)
      | (Lit _, Add _) -> b <+> a
      | (Add (x, Lit m), Lit n) | (Add (Lit m, x), Lit n) -> Add (x, Lit (m+n))
      | (Add (x, Lit m), Add (y, Lit n)) -> Add (Add(x, y), Lit (m+n))
      | _ -> Add (a, b)
      )
  | "mul" ->
      (match a, b with
        | (Lit 0, _) | (_, Lit 0) -> Lit 0
        | (Lit 1, x) | (x, Lit 1) -> x
        | (Lit m, Lit n) -> Lit (m * n)
        | Add (a', b'), x | x, Add (a', b') -> (x <*> a') <+> (x <*> b')

        (* associativity/commutativity with lits *)
        | Lit m, Mul (Lit n, x) | Lit m, Mul (x, Lit n) | Mul (x, Lit n), Lit m | Mul (Lit n, x), Lit m ->
            Mul (Lit (m*n), x)

        | _ -> Mul (a, b)
      )
  | "mod" ->
      (match a, b with
      | (Lit 0, _) -> Lit 0
      | (_, Lit 1) -> Lit 0
      (* distribute mod over addition; TODO this may be dangerous.  ignore for now *)
      | (Add (a', b'), m) -> (a' <%> m) <+> (b' <%> m)
      | (Digit _, Lit n) when n > 9 -> a
      | (Lit m, Lit n) when n > m -> a
      | (Lit m, Lit n) -> Lit (m mod n)
      | (Eql _, Lit n) | (Neq _, Lit n) when n > 1 -> a
      | (Mul (a', b'), m) -> (a' <%> m) <*> (b' <%> m)

      | _ -> Mod (a, b)
      )
  | "div" ->
      (match a, b with
      | (x, Lit 1) -> x
      (* cannot distribute, because floor *)
      (*| (Add (a', b'), c) -> (a' </> c) <+> (b' </> c)
      *)
      | Lit m, Lit n when m mod n = 0 -> Lit (m/n)
      | Mul (Lit m, x), Lit n when m mod n = 0 -> Lit (m/n) <*> x
      (*| Mul (Lit m, x), _ -> (Lit m </> b) <*> x*)
      | _ -> Div (a, b)
      )
  | "eql" ->
      (match a, b with
      | (Lit n, Digit _) | (Digit _, Lit n) when n <= 0 || n >= 10 -> Lit 0
      | (Lit a, Lit b) -> Lit (Bool.to_int (a = b))
      | (Lit 0, Eql (a', b')) | (Eql (a', b'), Lit 0) -> Neq (a', b')

      (* d + n never equals d' if |n| >= 9 *)
      | (Add (Digit _, Lit n), Digit _)
      | (Add (Lit n, Digit _), Digit _)
      | (Digit _, Add (Digit _, Lit n))
      | (Digit _, Add (Lit n, Digit _)) when abs n >= 9 -> Lit 0

      | _ -> Eql (a, b)
      )
  | _ -> failwith "invalid operator name"
and (<+>) a = operate "add" a
and (<*>) a = operate "mul" a
and (<%>) a = operate "mod" a
and (</>) a = operate "div" a
and (<=>) a = operate "eql" a

let execute =
  List.fold_left
  ( fun frame line ->
    let set = set frame.state in
    let get = get frame.state in
    match String.split ~by:" " line with
    | ["inp"; c] ->
        { state = set c @@ Digit frame.digit
        ; digit = frame.digit + 1
        }
    | ["add" | "mul" | "div" | "mod" | "eql" as op; a; b] ->
        {frame with state = set a @@ operate op (get a) (get b)}
    | _ ->
        failwith "invalid args"
  )
  {state = {x=Lit 0; y=Lit 0;z=Lit 0;w=Lit 0}; digit=0 }
  (List.take 900 lines)

let prec = function
  | Digit _ | Lit _ -> 0
  | Mul _ | Mod _ | Div _ -> 1
  | Add _ -> 2
  | Eql _ | Neq _ -> 3

let paren v s = match v with
  | Digit _ | Lit _ -> s
  | Mul _ | Mod _ | Div _ -> "(" ^ s ^ ")"
  | Add _ -> "[" ^ s ^ "]"
  | Eql _ | Neq _ -> "{" ^ s ^ "}"

let rec show value =
  let s v =
    let q = show v in
    if prec v >= prec value then
      paren v q
    else q
  in
  match value with
  | Digit n -> "d" ^ Int.to_string n
  | Lit n -> Int.to_string n
  | Add (a, b) -> s a ^ "+" ^ s b
  | Mul (a, b) -> s a ^ " " ^ s b
  | Mod (a, b) -> s a ^ "%" ^ s b
  | Div (a, b) -> s a ^ "/" ^ s b
  | Eql (a, b) -> s a ^ "==" ^ s b
  | Neq (a, b) -> s a ^ "!=" ^ s b

let print_frame frame =
  print_endline @@ "frame [inp i=" ^ Int.to_string frame.digit ^ "]"
  ; print_endline @@ "w: " ^ show frame.state.w
  ; print_endline @@ "x: " ^ show frame.state.x
  ; print_endline @@ "y: " ^ show frame.state.y
  ; print_endline @@ "z: " ^ show frame.state.z

let () =
  execute |> print_frame
