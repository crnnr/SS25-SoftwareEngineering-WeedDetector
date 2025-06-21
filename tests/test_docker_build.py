import unittest
import subprocess

class TestDockerBuild(unittest.TestCase):
    def test_docker_image_build(self):
        result = subprocess.run(['docker', 'build', '-t', 'my-image', '.'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Successfully built', result.stdout)

if __name__ == '__main__':
    unittest.main()