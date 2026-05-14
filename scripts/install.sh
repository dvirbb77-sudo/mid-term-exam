#!/usr/bin/env bash
####################################################
# version: 1.0
# created by: Bibi
# purpose: Setup nginx for the mid-term exam project
# date: 2026-05-11
#####################################################
set -euo pipefail


readonly APP_NAME="status-dashboard"
readonly PORT=${PORT:-5000}
readonly VERSION=${VERSION:-"1.1.0"}
readonly API_KEY=${API_KEY:-""} 

readonly NGINX_SRC="./nginx/status-dashboard.conf"
readonly NGINX_AVAIL="/etc/nginx/sites-available/status-dashboard"
readonly NGINX_ENABL="/etc/nginx/sites-enabled/status-dashboard"
readonly NGINX_DEFAULT="/etc/nginx/sites-enabled/default"


log() {
    echo -e "\033[1;32m[INFO]\033[0m $1"
}

error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1" >&2
    exit 1
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root. Please use: sudo ./install.sh"
    fi
}

validate_env() {
    if [[ -z "$API_KEY" ]]; then
        error "API_KEY is not set. Usage: API_KEY=secret123 sudo ./install.sh"
    fi
}

setup_container() {
    log "Building Docker image: $APP_NAME..."
    docker build -t "$APP_NAME" .

    log "Cleaning up old containers..."
    docker rm -f "$APP_NAME" 2>/dev/null || true

    log "Starting new container on 127.0.0.1:$PORT..."
    docker run -d \
        --name "$APP_NAME" \
        --restart unless-stopped \
        -p 127.0.0.1:"$PORT":"$PORT" \
        -e PORT="$PORT" \
        -e VERSION="$VERSION" \
        -e API_KEY="$API_KEY" \
        "$APP_NAME"
}

setup_nginx() {
    log "Configuring Nginx..."

    if [[ ! -f "$NGINX_SRC" ]]; then
        error "Nginx config source not found at $NGINX_SRC"
    fi

    rm -f "$NGINX_DEFAULT"

    cp "$NGINX_SRC" "$NGINX_AVAIL"
    ln -sf "$NGINX_AVAIL" "$NGINX_ENABL"

    log "Validating Nginx configuration..."
    if nginx -t; then
        systemctl enable nginx
        systemctl restart nginx
    else
        error "Nginx configuration validation failed."
    fi
}

main() {
    check_root
    validate_env
    
    log "Starting installation of $APP_NAME v$VERSION..."
    
    setup_container
    setup_nginx

    local ip_addr
    ip_addr=$(hostname -I | awk '{print $1}')
    
    echo "--------------------------------------------------"
    log "INSTALLATION COMPLETE"
    log "Service reachable at: http://$ip_addr/"
    echo "--------------------------------------------------"
}

main "$@"
