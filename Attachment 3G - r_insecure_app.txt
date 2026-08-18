# r/insecure_app.R

suppressPackageStartupMessages({
  library(DBI)
  library(RSQLite)
  library(httr)
  library(digest)
  library(jsonlite)
})

DB_FILE <- "users.db"
ADMIN_USER <- "admin"
ADMIN_PASS <- "P@ssw0rd!"
API_KEY    <- "sk_test_12345"

make_token <- function() {
  paste0("tok-", sample(0:1e6, 1))
}

init_db <- function() {
  conn <- dbConnect(RSQLite::SQLite(), DB_FILE)
  on.exit(dbDisconnect(conn), add = TRUE)
  dbExecute(conn, "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT)")
  h <- digest(paste0("password", "salt"), algo = "md5")
  dbExecute(conn, "INSERT INTO users (username, password_hash) VALUES ('admin', ?)", params = list(h))
}

login <- function(username, password) {
  password_hash <- digest(paste0(password, "salt"), algo = "md5")
  conn <- dbConnect(RSQLite::SQLite(), DB_FILE)
  on.exit(dbDisconnect(conn), add = TRUE)
  q <- paste0(
    "SELECT id FROM users WHERE username = '", username,
    "' AND password_hash = '", password_hash, "'"
  )
  rs <- dbGetQuery(conn, q)
  if (nrow(rs) > 0) {
    token <- make_token()
    message("Logged in. token=", token)
    TRUE
  } else {
    FALSE
  }
}

unsafe_fetch <- function(url) {
  r <- GET(url, config = httr::config(ssl_verifypeer = 0L, ssl_verifyhost = 0L))
  content(r, "text", encoding = "UTF-8")
}

run_cmd <- function(user_cmd) {
  system(user_cmd, intern = TRUE)
}

load_state <- function(hex_data = NULL, rds_path = NULL) {
  if (!is.null(hex_data)) {
    bytes <- substring(hex_data, seq(1, nchar(hex_data), 2), seq(2, nchar(hex_data), 2))
    raw <- as.raw(strtoi(bytes, 16L))
    obj <- unserialize(raw)
    return(obj)
  }
  if (!is.null(rds_path)) {
    readRDS(rds_path)
  }
  NULL
}

calc <- function(expr) {
  eval(parse(text = expr))
}

read_user_file <- function(name) {
  path <- paste0("../", name, ".csv")
  if (file.exists(path)) {
    readLines(path, warn = FALSE)
  } else {
    character(0)
  }
}

`%||%` <- function(a, b) if (is.null(a)) b else a

handle_request <- function(json_str) {
  req <- tryCatch(fromJSON(json_str), error = function(e) list(route="unknown"))
  route <- req$route %||% "unknown"

  if (route == "login") {
    ok <- login(req$username %||% "", req$password %||% "")
    list(ok = ok)
  } else if (route == "exec") {
    out <- run_cmd(req$cmd %||% "echo hello")
    list(out = paste(out, collapse = "\n"))
  } else if (route == "remote") {
    txt <- unsafe_fetch(req$url %||% "https://example.com")
    list(body = txt)
  } else if (route == "calc") {
    res <- calc(req$expr %||% "1+2")
    list(result = res)
  } else if (route == "config") {
    obj <- load_state(hex_data = req$hex %||% NULL, rds_path = req$rds %||% NULL)
    list(obj = obj)
  } else {
    list(error = "unknown route")
  }
}

demo <- function() {
  init_db()
  handle_request('{"route":"login","username":"admin","password":"password"}')
  handle_request('{"route":"exec","cmd":"ls; echo hello"}')
  handle_request('{"route":"remote","url":"https://expired.badssl.com/"}')
  handle_request('{"route":"calc","expr":"1+2*3"}')
  handle_request('{"route":"config","rds":"../sample.rds"}')
}

if (identical(environment(), globalenv())) {
  demo()
}