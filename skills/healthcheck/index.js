const path = require('path');

// Health check skill implementation
module.exports = {
    name: 'healthcheck',
    description: 'Simple skill health checker for AEF-OMP skills - validates SKILL.md files and checks -stable suffix in versions',
    userInvocable: true,
    tools: ['read', 'write', 'edit', 'bash', 'glob'],

    async execute(context, params = {}) {
        // Execute the healthcheck.py script
        const scriptPath = path.join(__dirname, 'healthcheck.py');

        const { exec } = require('child_process');

        return new Promise((resolve, reject) => {
            const command = `python3 ${scriptPath}`;

            const child = exec(command, {
                cwd: process.cwd(), // Use current working directory
                maxBuffer: 10 * 1024 * 1024, // 10MB buffer
                env: {
                    ...process.env,
                    PATH: process.env.PATH + ':' + path.dirname(scriptPath),
                }
            }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(`Health check failed: ${error.message}\n${stderr}`));
                } else {
                    resolve({
                        success: true,
                        output: stdout,
                        error: stderr,
                        command: command
                    });
                }
            });

            // Set timeout to prevent hanging
            setTimeout(() => {
                child.kill('SIGTERM');
                reject(new Error('Health check timed out after 30 seconds'));
            }, 30000);
        });
    },

    // Optional: Additional methods that might be needed
    validate(spec) {
        return spec && typeof spec === 'object' && spec.name === 'healthcheck';
    }
};