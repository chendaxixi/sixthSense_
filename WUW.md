#WUW
---
##基本类介绍

	1.	SizeR：
	成员：
		_cx/Width：宽
		_cy/Height：高
	2.	PointR:
	成员：
		X：X坐标
		Y：Y坐标
		T：绘制该点的时刻
	3.	RectangleR：
	成员：
		Digits：保留的小数位数
		_x/X：左上角x坐标
		_y/Y：左上角y坐标
		_width/Width：宽
		_height/Height：高
		TopLeft:左上角点
		BottomRight:右下角点
		Center：中心点
		MaxSide：宽/高中较长的
		MinSide：宽/高中较短的
		Diagonal：对角线长
	4.	Utils：
	成员：
		_rand：Random类对象，用于产生随机数
		FindBox(ArrayList points)：返回包络points点列的矩形
		Distance(PointR p1, PointR p2)：返回p1,p2点距离
		Centroid(ArrayList points)：返回points点列的几何中心点
		PathLength(ArrayList points)：返回points点列表示的路径的长度
		AngleInDegrees(PointR start, PointR end, bool positiveOnly)：返回start所在水平线与start-end连线的夹角，顺时针为正；positiveOnly为true则返回值必须为正数(若为负数则+360);夹角以度数表示
		AngleInRadians(PointR start, PointR end, bool positiveOnly)：与AngleInRadians相似，返回值为弧度值
		Rad2Deg(double rad)：返回弧度值对应的角度值
		Deg2Rad(double deg)：返回角度值对应的弧度值
		RotateByDegrees(ArrayList points, double degrees)：返回points点列绕其中心点顺时针旋转degrees角度后所得点列
		RotateByRadians(ArrayList points, double radians)：返回points点列绕其中心点顺时针旋转radians弧度后所得点列
		RotatePoint(PointR p, PointR c, double radians)：返回p点绕c点顺时针旋转radians弧度后所得点
		TranslateBBoxTo(ArrayList points, PointR toPt)：平移点列，使得点列的包络矩形以toPt为左上角
		TranslateCentroidTo(ArrayList points, PointR toPt)：平移点列，使点列以toPt为中心点
		TranslateBy(ArrayList points, SizeR sz)：平移sz向量
		ScaleTo(..)：以原点作位似变换，使包络面矩形变为..
		ScaleBy(..)：以原点作位似变换，使包络面矩形变为原来的sz倍
		Resample(ArrayList points, int n)：从点列points中取出n个样点
		PathDistance(ArrayList path1, ArrayList path2)：计算两条路径的距离，实际就是计算两种图案的相似度
		Random(int low, int high)：产生一个low-high间的随机数
		Random(int low, int high, int num）：产生num个不重复的low-high间的随机数
	5.	NBestList：与所画手势相近的手势列表
	成员：
		NBestResult类：与所画手势比较的结果类
			_name：手势的名字
			_score：相似度
			_distance：所画手势与名为_name的手势达成最相似时的距离
			_angle：所画手势与名为_name的手势达成最相似时的旋转角度
	6.	Gesture：手势类
	成员：
		Name：如clock03
		RawPoints：表示一个手势的全部节点
		Points：取样节点(用于进行匹配)
	7.	Category：手势集合类
	成员：
		_name/Name：如clock
		_prototypes：属于该集合的手势列表，如clock01,clock02,clock03
		NumExamples：属于该集合的手势个数
		AddExample(Gesture p)：往集合中添加手势
	8.	GeometricRecognizer：手势识别类
	成员：
		Phi：黄金分割比例
		tolerance：能容忍的最低相似度(低于tolerance的相似度就无法识别)
		Recognize(ArrayList points)：找出与点列points对应的手势相似的手势列表，返回值为NBestList类型；具体方法为将点列放缩平移到与数据库中手势相同后，求各种旋转角度下两点列的距离(手势的相似度)
		GoldenSectionSearch/HillClimbSearch/FullSearch：三种可以求出俩点列的最终相似度的方法
		AssembleBatch(string[] filenames)：将若干手势文件预处理成各个category,并保证每个category的手势数目一致

##架构介绍

	1.	class文件夹存放基础类
	2.	WUW.Designer.cs用于生成相应的控件以及设置控件的响应函数
	3.	WUW.cs具体编写相应的响应函数
	4.	界面的显示：通过控件的Hide,Show实现，实现布置好所有控件(时钟、天气预报这些也都是控件)
	5.	故一个控件的显示和交互一共需要以下步骤：
		1.	在WUW.Designer.cs中声明控件变量(如：
			private System.Windows.Forms.Button buttonWeatherDemo;)
		2.	new出控件对象(如：
			this.buttonWeatherDemo = new System.Windows.Forms.Button();)
		3.	初始化控件的字体、大小、位置等(如：
			this.buttonWeatherDemo.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.buttonWeatherDemo.Location = new System.Drawing.Point(6, 133);
            this.buttonWeatherDemo.Name = "buttonWeatherDemo";
            this.buttonWeatherDemo.Size = new System.Drawing.Size(129, 26);
            this.buttonWeatherDemo.TabIndex = 37;
            this.buttonWeatherDemo.Text = "Weather";
            this.buttonWeatherDemo.UseVisualStyleBackColor = true;)
		4.	为控件添加响应函数(如：	this.buttonWeatherDemo.Click += new 	System.EventHandler	(this.buttonWeatherDemo_Click);)
		5.	在WUW.cs中定义该响应函数
	6.	具体功能分为两个步骤：
		1.	画出相应手势，进行识别(鼠标单击状态为绘制手势模式，若是采用标志物，则是M表示鼠标，N不在表示单击，N在表示松开)
		2.	进入该功能模式(如进入Photo Demo)，此时也可再做出相应动作，调用Demo中更具体的功能(如拍照)
	7.	总结：若想要添加一个新的功能，需要以下操作：
		1.	设计新功能界面(控件组成)
		2.	添加鼠标响应函数
		3.	添加标志物移动响应函数，设定具体动作(此时的动作指的是MNOP四个标志物的距离变化)
		4.	添加手势文件.xml(此时的手势指的是鼠标(M标志物)的移动轨迹)

##重要函数介绍

	1.	void m_OnChange(object sender, MarkerEventArgs e)当M移动时，就会调用该函数，根据当前的不同模式，有不同的手势判断
	2.	handSign_NoN():表示如果M在N不在，就为鼠标左击状态，如果N在，则为鼠标松开状态
	3.	#region Marker HandSigns Functions：标志物配合的相关手势函数定义区域
	4.	WUW_MouseDown/WUW_MouseMove/WUW_MouseUp：鼠标响应函数，就是绘制手势的相关函数