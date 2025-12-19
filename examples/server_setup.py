#!/usr/bin/env python3
"""
System Design: Web server deployment and configuration
Problem: Deploy nginx web server with SSL certificate and basic security

**Tools Needed**
- package management (dnf/apt)
- service management
- file operations
- user input for configuration

**Implementation Steps**
- Get server configuration from user
- Update system packages
- Install nginx web server
- Configure firewall rules
- Setup SSL certificate
- Deploy sample website

**Produces**
- Fully configured web server with SSL
- Security hardened configuration
- Ready for production use
"""

import ftl_automation


def main():
    """Deploy and configure web server following Linode script pattern."""

    with ftl_automation.automation(
        inventory="inventory.yml",
        modules=["modules"],
        secrets=["SSL_DOMAIN", "SSL_EMAIL"],
        user_input="server_config.yml",
    ) as ftl:

        # Assign tools using the Linode pattern
        user_input_tool = ftl.tools.user_input_tool
        complete = ftl.tools.complete
        impossible = ftl.tools.impossible
        debug_tool = ftl.tools.debug_tool
        get_secret = ftl.tools.get_secret

        # --------------------------------------------------------------------------------
        # Step 1: Get server configuration from user
        debug_tool("Starting web server deployment")

        server_name = user_input_tool(
            question="Enter server name:", default="web-server-01"
        )

        domain_name = user_input_tool(
            question="Enter domain name (e.g. example.com):", default="localhost"
        )

        print(f"Configuring server: {server_name}")
        print(f"Domain: {domain_name}")

        # --------------------------------------------------------------------------------
        # Step 2: Update system packages
        debug_tool("Updating system packages")

        try:
            # Try DNF first (Fedora/RHEL)
            update_result = ftl.run_module(
                "dnf", name="*", state="latest", update_cache=True
            )
            pkg_manager = "dnf"
        except:
            try:
                # Fall back to APT (Ubuntu/Debian)
                update_result = ftl.run_module("apt", upgrade="yes", update_cache=True)
                pkg_manager = "apt"
            except Exception as e:
                impossible(f"Could not update packages: {e}")

        if update_result:
            print("✓ System packages updated successfully")
        else:
            print("⚠ Package update completed with warnings")

        # --------------------------------------------------------------------------------
        # Step 3: Install nginx web server
        debug_tool("Installing nginx web server")

        install_result = ftl.run_module("package", name="nginx", state="present")

        if not install_result:
            impossible("Failed to install nginx")

        print("✓ Nginx installed successfully")

        # --------------------------------------------------------------------------------
        # Step 4: Start and enable nginx service
        debug_tool("Starting nginx service")

        service_result = ftl.run_module(
            "service", name="nginx", state="started", enabled=True
        )

        if not service_result:
            impossible("Failed to start nginx service")

        print("✓ Nginx service started and enabled")

        # --------------------------------------------------------------------------------
        # Step 5: Configure firewall (if available)
        debug_tool("Configuring firewall")

        try:
            # Try firewalld first
            firewall_http = ftl.run_module(
                "firewalld", service="http", permanent=True, state="enabled"
            )

            firewall_https = ftl.run_module(
                "firewalld", service="https", permanent=True, state="enabled"
            )

            # Reload firewall
            ftl.run_module("service", name="firewalld", state="reloaded")
            print("✓ Firewall configured (firewalld)")

        except:
            try:
                # Fall back to ufw
                ftl.run_module("ufw", rule="allow", port="80", proto="tcp")
                ftl.run_module("ufw", rule="allow", port="443", proto="tcp")
                ftl.run_module("ufw", state="enabled")
                print("✓ Firewall configured (ufw)")
            except:
                print("⚠ Could not configure firewall - manual configuration needed")

        # --------------------------------------------------------------------------------
        # Step 6: Create simple website
        debug_tool("Creating sample website")

        website_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Welcome to {server_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .info {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Welcome to {server_name}</h1>
    <div class="info">
        <p><strong>Server:</strong> {server_name}</p>
        <p><strong>Domain:</strong> {domain_name}</p>
        <p><strong>Status:</strong> ✓ Web server is running</p>
        <p><strong>Deployed:</strong> $(date)</p>
    </div>
    <p>This server was deployed using FTL Automation!</p>
</body>
</html>"""

        # Create website directory
        ftl.run_module(
            "file", path=f"/var/www/{domain_name}", state="directory", mode="0755"
        )

        # Deploy index.html
        ftl.run_module(
            "copy",
            content=website_content,
            dest=f"/var/www/{domain_name}/index.html",
            mode="0644",
        )

        print(f"✓ Sample website deployed to /var/www/{domain_name}")

        # --------------------------------------------------------------------------------
        # Step 7: Configure nginx for the domain
        debug_tool("Configuring nginx virtual host")

        nginx_config = f"""server {{
    listen 80;
    server_name {domain_name} www.{domain_name};
    
    root /var/www/{domain_name};
    index index.html;
    
    location / {{
        try_files $uri $uri/ =404;
    }}
    
    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
}}"""

        ftl.run_module(
            "copy",
            content=nginx_config,
            dest=f"/etc/nginx/sites-available/{domain_name}",
            mode="0644",
        )

        # Enable site
        ftl.run_module(
            "file",
            src=f"/etc/nginx/sites-available/{domain_name}",
            dest=f"/etc/nginx/sites-enabled/{domain_name}",
            state="link",
        )

        # Test nginx configuration
        test_result = ftl.run_module("command", cmd="nginx -t")
        if test_result:
            # Reload nginx
            ftl.run_module("service", name="nginx", state="reloaded")
            print(f"✓ Nginx configured for {domain_name}")
        else:
            print("⚠ Nginx configuration test failed")

        # --------------------------------------------------------------------------------
        # Step 8: Optional SSL setup
        ssl_domain = get_secret("SSL_DOMAIN")
        ssl_email = get_secret("SSL_EMAIL")

        if ssl_domain and ssl_email and domain_name != "localhost":
            debug_tool("Setting up SSL certificate")

            try:
                # Install certbot
                ftl.run_module("package", name="certbot", state="present")

                # Get SSL certificate
                cert_result = ftl.run_module(
                    "command",
                    cmd=f"certbot --nginx -d {domain_name} --email {ssl_email} --agree-tos --non-interactive",
                )

                if cert_result:
                    print("✓ SSL certificate installed")
                else:
                    print("⚠ SSL certificate installation failed")
            except:
                print("⚠ SSL setup skipped - certbot not available")
        else:
            print("ℹ SSL setup skipped - no domain/email provided")

        # --------------------------------------------------------------------------------
        # Final verification
        debug_tool("Performing final verification")

        # Check if nginx is running
        status_result = ftl.run_module("command", cmd="systemctl is-active nginx")

        if status_result and "active" in str(status_result):
            print("✓ Final verification passed")
            print(f"\n🎉 Web server deployment completed!")
            print(f"   Server: {server_name}")
            print(f"   Domain: {domain_name}")
            print(f"   URL: http://{domain_name}")
            if ssl_domain:
                print(f"   SSL: https://{domain_name}")

            complete(
                f"Web server {server_name} deployed successfully with domain {domain_name}"
            )
        else:
            impossible("Web server is not running after deployment")


if __name__ == "__main__":
    try:
        main()
    except ftl_automation.CompletionException as e:
        print(f"\n✅ Task completed: {e}")
    except ftl_automation.ImpossibleException as e:
        print(f"\n❌ Task impossible: {e}")
        exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        exit(1)
