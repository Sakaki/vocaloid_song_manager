var app = new Vue({
  el: '#app',
  mounted () {
    this.loadMusics(false)
  },
  methods: {
    loadMusics (openDialog) {
      eel.load_musics(openDialog)((songInfoList) => {
        this.songInfoList = songInfoList
      })
    },
    saveSongInfoList () {
      eel.save_song_info_list(this.songInfoList)
    },
    previewFilename () {
      console.log('AAA')
      eel.set_rename_to(this.songInfoList)((result) => {
        console.log(result)
        this.songInfoList = result
      })
    }
  },
  data () {
    const typeColor = {
      title: '#b6d2e4',
      singer: '#b2e2cf',
      author: '#d8b8e6',
      other: '#ddd'
    }
    return {
      message: '',
      songInfoList: [],
      attributes: [
        {label: 'タイトル', value: 'title'},
        {label: 'シンガー', value: 'singer'},
        {label: '作者', value: 'author'},
        {label: 'その他', value: 'other'}
      ],
      typeColor: typeColor
    }
  }
})
