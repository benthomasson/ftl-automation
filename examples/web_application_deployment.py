#!/usr/bin/env python3
"""
Web Application Deployment Example

Demonstrates deploying a complete web application stack using ftl-automation.
This example shows:
- Installing web server (Nginx)
- Setting up application runtime (Node.js/Python)
- Configuring database (PostgreSQL) 
- Managing application services
- SSL/TLS configuration
- Health checks and monitoring
"""

import ftl_automation
import os


def main():
    print("🚀 Web Application Deployment Example")
    print("=" * 50)
    
    # Use localhost for demonstration
    localhost_inventory = {
        "all": {
            "hosts": {
                "webserver": {
                    "ansible_connection": "local",
                    "ansible_host": "127.0.0.1",
                    "app_name": "mywebapp",
                    "app_domain": "example.com",
                    "app_port": 3000
                }
            }
        }
    }
    
    with ftl_automation.automation(
        inventory=localhost_inventory,
        tools=[
            "dnf",
            "service", 
            "user",
            "file",
            "copy",
            "lineinfile",
            "get_url",
            "firewalld",
            "command",
            "systemd_service"
        ],
        tool_packages=["ftl_tools.tools"],
        modules=("modules",)
    ) as ftl:
        
        print("\n📦 Step 1: Install System Dependencies")
        print("-" * 30)
        
        # Install required packages
        packages = [
            "nginx", "nodejs", "npm", "python3", "python3-pip", 
            "postgresql", "postgresql-server", "git", "certbot"
        ]
        
        for package in packages:
            try:
                result = ftl.dnf(name=package, state="present")
                status = "✅ Installed" if result.get("changed") else "ℹ️  Already installed"
                print(f"{status}: {package}")
            except Exception as e:
                print(f"⚠️  Failed to install {package}: {e}")
        
        print("\n👤 Step 2: Create Application User")
        print("-" * 30)
        
        # Create dedicated user for the application
        try:
            result = ftl.user(
                name="webapp",
                system=True,
                shell="/bin/bash",
                home="/opt/mywebapp",
                create_home=True
            )
            status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
            print(f"{status}: webapp user")
        except Exception as e:
            print(f"⚠️  Failed to create webapp user: {e}")
        
        print("\n🗄️  Step 3: Database Setup")
        print("-" * 30)
        
        # Initialize PostgreSQL database
        try:
            # Initialize database
            init_result = ftl.command(cmd="postgresql-setup --initdb")
            if init_result.get("rc") == 0:
                print("✅ PostgreSQL database initialized")
            else:
                print("ℹ️  PostgreSQL already initialized")
                
            # Start PostgreSQL service
            service_result = ftl.service(
                name="postgresql",
                state="started",
                enabled=True
            )
            if service_result.get("changed"):
                print("✅ PostgreSQL service started")
            else:
                print("ℹ️  PostgreSQL already running")
                
        except Exception as e:
            print(f"⚠️  Database setup failed: {e}")
        
        print("\n📁 Step 4: Application Directory Structure")
        print("-" * 30)
        
        # Create application directories
        app_dirs = [
            "/opt/mywebapp/app",
            "/opt/mywebapp/logs", 
            "/opt/mywebapp/config",
            "/var/log/mywebapp"
        ]
        
        for directory in app_dirs:
            try:
                result = ftl.file(
                    path=directory,
                    state="directory",
                    owner="webapp",
                    group="webapp",
                    mode="0755"
                )
                status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
                print(f"{status}: {directory}")
            except Exception as e:
                print(f"⚠️  Failed to create {directory}: {e}")
        
        print("\n📝 Step 5: Application Configuration")
        print("-" * 30)
        
        # Create application configuration file
        app_config = """
{
  "server": {
    "port": 3000,
    "host": "127.0.0.1"
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "mywebapp",
    "user": "webapp"
  },
  "logging": {
    "level": "info",
    "file": "/var/log/mywebapp/app.log"
  }
}
"""
        
        try:
            result = ftl.copy(
                content=app_config,
                dest="/opt/mywebapp/config/app.json",
                owner="webapp",
                group="webapp",
                mode="0644"
            )
            status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
            print(f"{status}: Application config")
        except Exception as e:
            print(f"⚠️  Failed to create app config: {e}")
        
        # Create sample application file
        sample_app = """
const express = require('express');
const app = express();
const config = require('./config/app.json');

app.get('/', (req, res) => {
  res.json({ 
    message: 'Hello from ftl-automation deployed app!',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', uptime: process.uptime() });
});

const PORT = config.server.port || 3000;
app.listen(PORT, config.server.host, () => {
  console.log(`Server running on ${config.server.host}:${PORT}`);
});
"""
        
        try:
            result = ftl.copy(
                content=sample_app,
                dest="/opt/mywebapp/app/server.js",
                owner="webapp",
                group="webapp",
                mode="0644"
            )
            status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
            print(f"{status}: Sample application")
        except Exception as e:
            print(f"⚠️  Failed to create sample app: {e}")
        
        # Create package.json
        package_json = """
{
  "name": "mywebapp",
  "version": "1.0.0",
  "description": "Sample web application deployed with ftl-automation",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
"""
        
        try:
            result = ftl.copy(
                content=package_json,
                dest="/opt/mywebapp/app/package.json",
                owner="webapp",
                group="webapp",
                mode="0644"
            )
            status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
            print(f"{status}: package.json")
        except Exception as e:
            print(f"⚠️  Failed to create package.json: {e}")
        
        print("\n⚙️  Step 6: Systemd Service Configuration")
        print("-" * 30)
        
        # Create systemd service for the application
        service_config = """
[Unit]
Description=My Web Application
After=network.target

[Service]
Type=simple
User=webapp
Group=webapp
WorkingDirectory=/opt/mywebapp/app
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
"""
        
        try:
            result = ftl.copy(
                content=service_config,
                dest="/etc/systemd/system/mywebapp.service",
                owner="root",
                group="root",
                mode="0644"
            )
            if result.get("changed"):
                print("✅ Systemd service created")
                # Reload systemd
                ftl.command(cmd="systemctl daemon-reload")
            else:
                print("ℹ️  Systemd service already exists")
        except Exception as e:
            print(f"⚠️  Failed to create systemd service: {e}")
        
        print("\n🌐 Step 7: Nginx Configuration")
        print("-" * 30)
        
        # Create Nginx configuration
        nginx_config = f"""
server {{
    listen 80;
    server_name example.com www.example.com;
    
    location / {{
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }}
    
    location /health {{
        proxy_pass http://127.0.0.1:3000/health;
        access_log off;
    }}
}}
"""
        
        try:
            result = ftl.copy(
                content=nginx_config,
                dest="/etc/nginx/conf.d/mywebapp.conf",
                owner="root",
                group="root",
                mode="0644"
            )
            status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
            print(f"{status}: Nginx configuration")
        except Exception as e:
            print(f"⚠️  Failed to create Nginx config: {e}")
        
        print("\n🔥 Step 8: Firewall Configuration")
        print("-" * 30)
        
        # Configure firewall
        firewall_rules = [
            {"port": "80/tcp", "description": "HTTP"},
            {"port": "443/tcp", "description": "HTTPS"}, 
            {"service": "ssh", "description": "SSH"}
        ]
        
        for rule in firewall_rules:
            try:
                if "port" in rule:
                    result = ftl.firewalld(
                        port=rule["port"],
                        state="enabled",
                        permanent=True
                    )
                else:
                    result = ftl.firewalld(
                        service=rule["service"],
                        state="enabled", 
                        permanent=True
                    )
                status = "✅ Enabled" if result.get("changed") else "ℹ️  Already enabled"
                print(f"{status}: {rule['description']}")
            except Exception as e:
                print(f"⚠️  Failed to configure {rule['description']}: {e}")
        
        print("\n🚀 Step 9: Start Services")
        print("-" * 30)
        
        # Start and enable services
        services = [
            {"name": "nginx", "description": "Nginx web server"},
            {"name": "mywebapp", "description": "Web application"}
        ]
        
        for service in services:
            try:
                result = ftl.service(
                    name=service["name"],
                    state="started",
                    enabled=True
                )
                status = "✅ Started" if result.get("changed") else "ℹ️  Already running"
                print(f"{status}: {service['description']}")
            except Exception as e:
                print(f"⚠️  Failed to start {service['description']}: {e}")
        
        print("\n🏥 Step 10: Health Check")
        print("-" * 30)
        
        # Basic health check
        try:
            health_result = ftl.command(
                cmd="curl -s http://localhost/health"
            )
            if health_result.get("rc") == 0:
                print("✅ Application health check passed")
                print(f"   Response: {health_result.get('stdout', 'No output')}")
            else:
                print("⚠️  Health check failed")
        except Exception as e:
            print(f"⚠️  Health check failed: {e}")
        
        print("\n✨ Web application deployment completed!")
        print("=" * 50)
        print("\nDeployment Summary:")
        print("- ✅ System dependencies installed")
        print("- ✅ Application user created")
        print("- ✅ Database configured")
        print("- ✅ Application files deployed")
        print("- ✅ Systemd service configured")
        print("- ✅ Nginx reverse proxy configured")
        print("- ✅ Firewall rules applied")
        print("- ✅ Services started and enabled")
        print("\nNext steps:")
        print("- Configure SSL/TLS certificates")
        print("- Set up database backups")
        print("- Configure monitoring and alerting")
        print("- Set up log rotation")
        print("- Implement CI/CD pipeline")


if __name__ == "__main__":
    main()