pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'chobi'
gnome = import('gnome')

gnome.compile_resources('chobi',
  'chobi.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'chobi.in',
  output: 'chobi',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

chobi_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'peoplePage.py',
  'libraryPage.py',
  'dayPage.py',
  'placesPage.py',
  'favouritesPage.py',
]

install_data(chobi_sources, install_dir: moduledir)
